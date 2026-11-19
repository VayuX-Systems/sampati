# SPDX-License-Identifier: Apache-2.0
"""Plugin signing and verification."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


class PluginSigner:
    """Signs plugin packages using cosign."""

    def __init__(self, key_path: str | None = None, password: str | None = None) -> None:
        self.key_path = key_path
        self.password = password

    def sign_plugin(self, plugin_dir: Path, output_path: Path | None = None) -> Path:
        """Sign a plugin directory using cosign."""
        if output_path is None:
            output_path = plugin_dir / "plugin.sig"
        
        # Create a manifest of the plugin contents for signing
        manifest = self._create_manifest(plugin_dir)
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest, f, sort_keys=True)
            manifest_path = Path(f.name)
        
        try:
            cmd = [
                "cosign", "sign-blob",
                "--yes",
            ]
            
            if self.key_path:
                cmd.extend(["--key", self.key_path])
            if self.password:
                cmd.extend(["--password", self.password])
            
            cmd.append(str(manifest_path))
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            signature = result.stdout.strip()
            
            # Write signature file
            output_path.write_text(signature)
            return output_path
        finally:
            manifest_path.unlink(missing_ok=True)

    def _create_manifest(self, plugin_dir: Path) -> dict[str, Any]:
        """Create a manifest of all files in the plugin directory."""
        files = []
        for file_path in plugin_dir.rglob("*"):
            if file_path.is_file() and file_path.name != "plugin.sig":
                rel_path = file_path.relative_to(plugin_dir)
                content = file_path.read_bytes()
                file_hash = hashlib.sha256(content).hexdigest()
                files.append({
                    "path": str(rel_path),
                    "sha256": file_hash,
                    "size": len(content),
                })
        
        return {
            "version": "1",
            "files": sorted(files, key=lambda x: x["path"]),
        }


def verify_plugin_signature(plugin_dir: Path, signature_path: Path | None = None, public_key: str | None = None) -> bool:
    """Verify a plugin's signature using cosign."""
    if signature_path is None:
        signature_path = plugin_dir / "plugin.sig"
    
    if not signature_path.exists():
        return False
    
    # Create manifest
    signer = PluginSigner()
    manifest = signer._create_manifest(plugin_dir)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(manifest, f, sort_keys=True)
        manifest_path = Path(f.name)
    
    try:
        cmd = [
            "cosign", "verify-blob",
        ]
        
        if public_key:
            cmd.extend(["--key", public_key])
        
        signature = signature_path.read_text().strip()
        cmd.extend(["--signature", signature, str(manifest_path)])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    finally:
        manifest_path.unlink(missing_ok=True)
