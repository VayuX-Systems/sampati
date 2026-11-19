# SPDX-License-Identifier: Apache-2.0
"""Plugin host for running plugins out-of-process with sandboxing."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PluginStatus(Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"
    PENDING_APPROVAL = "pending_approval"


class PermissionScope(Enum):
    NETWORK = "network"
    FILESYSTEM_READ = "filesystem_read"
    FILESYSTEM_WRITE = "filesystem_write"
    SECRETS = "secrets"


@dataclass
class PluginPermission:
    scope: PermissionScope
    allowed: list[str] = field(default_factory=list)  # e.g., hostnames for network, paths for filesystem


@dataclass
class PluginManifest:
    id: str
    name: str
    type: str  # connector, scanner, notifier, pack, report-template
    version: str
    protocol: str = "v1"
    licence: str = ""
    permissions: dict[str, list[str]] = field(default_factory=dict)
    config: list[dict[str, Any]] = field(default_factory=list)
    produces: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PluginInstall:
    id: str = field(default_factory=lambda: "pinst_" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
    organisation_id: str = ""
    plugin_id: str = ""
    plugin_version: str = ""
    manifest: PluginManifest | None = None
    config: dict[str, Any] = field(default_factory=dict)
    status: PluginStatus = PluginStatus.PENDING_APPROVAL
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PluginCredential:
    id: str = field(default_factory=lambda: "pcred_" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
    plugin_install_id: str = ""
    encrypted_secret: str = ""
    key_id: str = ""
    last_rotated_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PluginSandbox:
    """
    Sandbox for running plugins out-of-process.

    In production, this would use containers (gVisor, firecracker, or Docker
    with network namespace isolation) and enforce:
    - Network allow-list
    - Filesystem access controls
    - CPU/memory limits
    - No access to host secrets or other plugin credentials
    """

    def __init__(self, plugin_install: PluginInstall) -> None:
        self.plugin_install = plugin_install
        self.manifest = plugin_install.manifest

    def validate_permissions(self) -> list[str]:
        """Validate that the plugin's requested permissions are acceptable."""
        errors = []
        if not self.manifest:
            errors.append("No manifest available")
            return errors

        # Check network allowlist
        network_allowlist = self.manifest.permissions.get("network_allowlist", [])
        for host in network_allowlist:
            if not self._is_valid_hostname(host):
                errors.append(f"Invalid hostname in network_allowlist: {host}")

        # Check scopes are read-only
        scopes = self.manifest.permissions.get("scopes", [])
        for scope in scopes:
            if not scope.startswith("read:"):
                errors.append(f"Only read-only scopes allowed, got: {scope}")

        return errors

    def _is_valid_hostname(self, hostname: str) -> bool:
        """Basic hostname validation."""
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

    async def run_collect(self, organisation_id: str, config: dict[str, Any], window_start: str, window_end: str):
        """
        Run the plugin's collect method.

        In production, this would spawn a container and communicate via gRPC/HTTP.
        """
        # TODO: Implement container spawn and gRPC communication
        raise NotImplementedError("Plugin sandbox execution not implemented in alpha")

    async def run_health_check(self) -> dict[str, Any]:
        """Run health check on the plugin."""
        # TODO: Implement
        return {"status": "unknown", "message": "health check not implemented", "checked_at": datetime.now(timezone.utc).isoformat()}

    async def validate_config(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate plugin configuration."""
        # TODO: Call plugin's ValidateConfig RPC
        return True, []
