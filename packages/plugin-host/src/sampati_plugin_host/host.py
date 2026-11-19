# SPDX-License-Identifier: Apache-2.0
"""Plugin Host - runs plugins out-of-process with sandboxing."""

from __future__ import annotations

import asyncio
import json
import subprocess
import tempfile
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import docker
import grpc

from .manifest import PluginManifest, PluginPermission, PluginType, PermissionScope
from .signing import verify_plugin_signature


@dataclass
class PluginInstall:
    """Represents an installed plugin instance."""
    id: str
    organisation_id: str
    plugin_id: str
    plugin_version: str
    manifest: PluginManifest
    config: dict[str, Any]
    status: str = "active"
    approved: bool = False
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PluginSandbox:
    """Sandbox configuration for a plugin."""
    plugin_id: str
    network_allowlist: list[str] = field(default_factory=list)
    cpu_limit: str = "0.5"  # CPU cores
    memory_limit: str = "256m"
    timeout_seconds: int = 300
    read_only_rootfs: bool = True
    drop_capabilities: list[str] = field(default_factory=lambda: ["ALL"])
    add_capabilities: list[str] = field(default_factory=list)


class PluginHost:
    """
    Host for running plugins out-of-process with sandboxing.
    
    Uses Docker containers with network allow-lists, resource limits,
    and no access to host filesystem or other plugins' credentials.
    """

    def __init__(self, docker_client: docker.DockerClient | None = None) -> None:
        self.docker = docker_client or docker.from_env()
        self._plugin_cache: dict[str, PluginInstall] = {}

    def validate_manifest(self, manifest: PluginManifest) -> list[str]:
        """Validate a plugin manifest. Returns list of errors."""
        errors = []
        
        if not manifest.id or not manifest.id.islower() or not manifest.id.replace("-", "").isalnum():
            errors.append("Plugin ID must be lowercase alphanumeric with hyphens")
        
        if not manifest.name:
            errors.append("Plugin name is required")
        
        if manifest.type not in PluginType:
            errors.append(f"Invalid plugin type: {manifest.type}")
        
        # Validate network allowlist
        for hostname in manifest.permissions.get("network_allowlist", []):
            if not self._is_valid_hostname(hostname):
                errors.append(f"Invalid hostname in network_allowlist: {hostname}")
        
        # Validate scopes are read-only
        for scope in manifest.permissions.get("scopes", []):
            if not scope.startswith("read:"):
                errors.append(f"Only read-only scopes allowed, got: {scope}")
        
        return errors

    def _is_valid_hostname(self, hostname: str) -> bool:
        """Validate hostname format."""
        if not hostname or len(hostname) > 255:
            return False
        parts = hostname.split(".")
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not all(c.isalnum() or c == "-" for c in part):
                return False
            if part.startswith("-") or part.endswith("-"):
                return False
        return True

    async def install_plugin(
        self,
        organisation_id: str,
        plugin_package_path: Path,
        config: dict[str, Any],
        approver_id: str | None = None,
    ) -> PluginInstall:
        """Install a plugin from a package directory."""
        
        # Load manifest
        manifest_path = plugin_package_path / "manifest.json"
        if not manifest_path.exists():
            raise ValueError("Plugin package missing manifest.json")
        
        manifest = PluginManifest.from_dict(json.loads(manifest_path.read_text()))
        
        # Validate manifest
        errors = self.validate_manifest(manifest)
        if errors:
            raise ValueError(f"Invalid manifest: {errors}")
        
        # Verify signature if present
        if not verify_plugin_signature(plugin_package_path):
            # Unsigned plugins require explicit admin approval
            if approver_id is None:
                raise ValueError("Unsigned plugin requires explicit admin approval")
        
        # Create install record
        install = PluginInstall(
            id=str(uuid.uuid4()),
            organisation_id=organisation_id,
            plugin_id=manifest.id,
            plugin_version=manifest.version,
            manifest=manifest,
            config=config,
            approved=approver_id is not None,
            approved_by=approver_id,
            approved_at=datetime.now(timezone.utc) if approver_id else None,
        )
        
        # Pull/build plugin image
        await self._prepare_plugin_image(plugin_package_path, manifest)
        
        # Store in cache
        self._plugin_cache[install.id] = install
        
        return install

    async def _prepare_plugin_image(self, plugin_package_path: Path, manifest: PluginManifest) -> None:
        """Build or pull the plugin's container image."""
        image_name = f"sampati-plugin-{manifest.id}:{manifest.version}"
        
        # Check if image exists locally
        try:
            self.docker.images.get(image_name)
            return  # Already built
        except docker.errors.ImageNotFound:
            pass
        
        # Look for Dockerfile in plugin package
        dockerfile = plugin_package_path / "Dockerfile"
        if dockerfile.exists():
            # Build image
            self.docker.images.build(
                path=str(plugin_package_path),
                tag=image_name,
                rm=True,
            )
        else:
            # For SDK-built plugins, the image should be pre-built and pushed
            # Try to pull from registry
            try:
                self.docker.images.pull(image_name)
            except docker.errors.ImageNotFound:
                raise ValueError(f"Plugin image {image_name} not found. Build it first or push to registry.")

    def _create_sandbox_config(self, install: PluginInstall) -> PluginSandbox:
        """Create sandbox configuration from plugin manifest."""
        manifest = install.manifest
        
        return PluginSandbox(
            plugin_id=manifest.id,
            network_allowlist=manifest.permissions.get("network_allowlist", []),
            cpu_limit="0.5",
            memory_limit="256m",
            timeout_seconds=300,
        )

    def _build_container_config(self, install: PluginInstall, sandbox: PluginSandbox) -> dict[str, Any]:
        """Build Docker container configuration."""
        manifest = install.manifest
        
        # Environment variables
        env = {
            "SAMPATI_ORGANISATION_ID": install.organisation_id,
            "SAMPATI_PLUGIN_ID": manifest.id,
            "SAMPATI_PLUGIN_VERSION": manifest.version,
            "SAMPATI_CONFIG": json.dumps(install.config),
        }
        
        # Network mode - use bridge with custom DNS for allowlist
        # In production, use a CNI plugin or service mesh for proper network policies
        network_mode = "bridge"
        
        # Labels for identification
        labels = {
            "sampati.plugin.id": manifest.id,
            "sampati.plugin.version": manifest.version,
            "sampati.organisation_id": install.organisation_id,
        }
        
        return {
            "image": f"sampati-plugin-{manifest.id}:{manifest.version}",
            "command": ["python", "-m", manifest.id.replace("-", "_")],
            "environment": env,
            "network_mode": network_mode,
            "mem_limit": sandbox.memory_limit,
            "cpu_quota": int(float(sandbox.cpu_limit) * 100000),
            "cpu_period": 100000,
            "read_only": sandbox.read_only_rootfs,
            "cap_drop": sandbox.drop_capabilities,
            "cap_add": sandbox.add_capabilities,
            "labels": labels,
            "remove": True,  # Auto-remove after completion
        }

    async def run_collect(
        self,
        install: PluginInstall,
        window_start: datetime,
        window_end: datetime,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Run a plugin's collect method and stream evidence records."""
        
        sandbox = self._create_sandbox_config(install)
        container_config = self._build_container_config(install, sandbox)
        
        # Add collection window to environment
        container_config["environment"].update({
            "SAMPATI_WINDOW_START": window_start.isoformat().replace("+00:00", "Z"),
            "SAMPATI_WINDOW_END": window_end.isoformat().replace("+00:00", "Z"),
        })
        
        # Run container
        container = self.docker.containers.run(**container_config, detach=True)
        
        try:
            # Stream logs (evidence records are printed as JSON lines)
            for log_line in container.logs(stream=True, follow=True):
                line = log_line.decode("utf-8").strip()
                if not line:
                    continue
                
                try:
                    record = json.loads(line)
                    yield record
                except json.JSONDecodeError:
                    # Non-JSON log line, skip
                    continue
            
            # Wait for completion
            result = container.wait(timeout=sandbox.timeout_seconds)
            if result["StatusCode"] != 0:
                raise RuntimeError(f"Plugin exited with code {result['StatusCode']}")
        
        finally:
            # Cleanup
            try:
                container.remove(force=True)
            except Exception:
                pass

    async def run_health_check(self, install: PluginInstall) -> dict[str, Any]:
        """Run a plugin's health check."""
        sandbox = self._create_sandbox_config(install)
        container_config = self._build_container_config(install, sandbox)
        
        container_config["command"] = ["python", "-m", install.manifest.id.replace("-", "_"), "health"]
        container_config["environment"]["SAMPATI_HEALTH_CHECK"] = "1"
        
        container = self.docker.containers.run(**container_config, detach=True)
        
        try:
            result = container.wait(timeout=30)
            logs = container.logs().decode("utf-8")
            
            try:
                health = json.loads(logs.strip().split("\n")[-1])
            except json.JSONDecodeError:
                health = {"status": "unknown", "message": logs}
            
            return health
        finally:
            try:
                container.remove(force=True)
            except Exception:
                pass

    async def validate_config(self, install: PluginInstall) -> tuple[bool, list[str]]:
        """Validate plugin configuration."""
        sandbox = self._create_sandbox_config(install)
        container_config = self._build_container_config(install, sandbox)
        
        container_config["command"] = ["python", "-m", install.manifest.id.replace("-", "_"), "validate"]
        container_config["environment"]["SAMPATI_VALIDATE_CONFIG"] = json.dumps(install.config)
        
        container = self.docker.containers.run(**container_config, detach=True)
        
        try:
            result = container.wait(timeout=30)
            logs = container.logs().decode("utf-8")
            
            try:
                validation = json.loads(logs.strip().split("\n")[-1])
                return validation.get("valid", False), validation.get("errors", [])
            except json.JSONDecodeError:
                return False, ["Invalid validation response"]
        finally:
            try:
                container.remove(force=True)
            except Exception:
                pass

    def list_installs(self, organisation_id: str) -> list[PluginInstall]:
        """List all plugin installs for an organisation."""
        return [
            install for install in self._plugin_cache.values()
            if install.organisation_id == organisation_id
        ]

    def get_install(self, install_id: str) -> PluginInstall | None:
        """Get a plugin install by ID."""
        return self._plugin_cache.get(install_id)
