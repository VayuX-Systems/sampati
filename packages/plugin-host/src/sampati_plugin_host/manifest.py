# SPDX-License-Identifier: Apache-2.0
"""Plugin manifest and permission models."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class PluginType(str, enum.Enum):
    CONNECTOR = "connector"
    SCANNER = "scanner"
    NOTIFIER = "notifier"
    PACK = "pack"
    REPORT_TEMPLATE = "report-template"


class PluginProtocol(str, enum.Enum):
    V1 = "v1"


class PermissionScope(str, enum.Enum):
    NETWORK = "network"
    FILESYSTEM_READ = "filesystem_read"
    FILESYSTEM_WRITE = "filesystem_write"
    SECRETS = "secrets"


@dataclass
class PluginPermission:
    """Permission granted to a plugin."""
    scope: PermissionScope
    allowed: list[str] = field(default_factory=list)  # hostnames for network, paths for filesystem


@dataclass
class PluginConfigField:
    """Configuration field definition for a plugin."""
    key: str
    label: str
    type: str  # string, secret, boolean, integer
    required: bool = False
    default: Any = None
    description: str = ""
    choices: list[str] = field(default_factory=list)


@dataclass
class PluginProduces:
    """What evidence/checks this plugin produces."""
    check: str
    supports_controls: list[str] = field(default_factory=list)
    schedule_default: str = "daily"


@dataclass
class PluginManifest:
    """Complete plugin manifest."""
    id: str
    name: str
    type: PluginType
    version: str
    protocol: PluginProtocol = PluginProtocol.V1
    licence: str = ""
    description: str = ""
    author: str = ""
    homepage: str = ""
    permissions: dict[str, list[str]] = field(default_factory=dict)  # scope -> allowed list
    config: list[PluginConfigField] = field(default_factory=list)
    produces: list[PluginProduces] = field(default_factory=list)
    schedule_default: str = "daily"
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "version": self.version,
            "protocol": self.protocol.value,
            "licence": self.licence,
            "description": self.description,
            "author": self.author,
            "homepage": self.homepage,
            "permissions": self.permissions,
            "config": [
                {
                    "key": c.key,
                    "label": c.label,
                    "type": c.type,
                    "required": c.required,
                    "default": c.default,
                    "description": c.description,
                    "choices": c.choices,
                }
                for c in self.config
            ],
            "produces": [
                {
                    "check": p.check,
                    "supports_controls": p.supports_controls,
                    "schedule_default": p.schedule_default,
                }
                for p in self.produces
            ],
            "schedule_default": self.schedule_default,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PluginManifest":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            type=PluginType(data["type"]),
            version=data["version"],
            protocol=PluginProtocol(data.get("protocol", "v1")),
            licence=data.get("licence", ""),
            description=data.get("description", ""),
            author=data.get("author", ""),
            homepage=data.get("homepage", ""),
            permissions=data.get("permissions", {}),
            config=[
                PluginConfigField(**c) for c in data.get("config", [])
            ],
            produces=[
                PluginProduces(**p) for p in data.get("produces", [])
            ],
            schedule_default=data.get("schedule_default", "daily"),
        )
