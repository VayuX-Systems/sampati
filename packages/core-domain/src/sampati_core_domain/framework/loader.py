# SPDX-License-Identifier: Apache-2.0
"""Framework loader and importer."""

from __future__ import annotations

import json
import yaml
from pathlib import Path
from typing import Any

from .models import Framework, Requirement, Control, ControlMapping


class FrameworkLoader:
    """Loads frameworks from YAML/JSON files."""

    def __init__(self) -> None:
        self.frameworks: dict[str, Framework] = {}
        self.requirements: dict[str, Requirement] = {}
        self.controls: dict[str, Control] = {}
        self.mappings: list[ControlMapping] = []

    def load_framework_file(self, path: Path) -> Framework:
        """Load a framework from a YAML or JSON file."""
        content = path.read_text()
        
        if path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(content)
        elif path.suffix == ".json":
            data = json.loads(content)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        return self._parse_framework(data)

    def _parse_framework(self, data: dict[str, Any]) -> Framework:
        """Parse framework data into model objects."""
        framework = Framework(
            id=data.get("id", ""),
            code=data.get("code", ""),
            name=data.get("name", ""),
            version=data.get("version", ""),
            status=data.get("status", "draft"),
            description=data.get("description", ""),
            source_url=data.get("source_url"),
        )
        
        # Parse requirements
        for req_data in data.get("requirements", []):
            requirement = Requirement(
                id=req_data.get("id", ""),
                framework_version_id=framework.id,
                reference=req_data.get("reference", ""),
                title=req_data.get("title", ""),
                text=req_data.get("text", ""),
                category=req_data.get("category"),
                parent_id=req_data.get("parent"),
                references=req_data.get("references", []),
            )
            self.requirements[requirement.id] = requirement
        
        return framework

    def load_controls(self, paths: list[Path]) -> None:
        """Load controls from YAML files."""
        for path in paths:
            content = path.read_text()
            data = yaml.safe_load(content)
            
            # Handle both single control and list of controls
            controls = data if isinstance(data, list) else [data]
            
            for ctrl_data in controls:
                control = Control(
                    id=ctrl_data.get("id", ""),
                    code=ctrl_data.get("code", ""),
                    title=ctrl_data.get("title", ""),
                    description=ctrl_data.get("description", ""),
                    category=ctrl_data.get("category", ""),
                    guidance=ctrl_data.get("guidance", ""),
                )
                self.controls[control.id] = control

    def load_mappings(self, paths: list[Path]) -> None:
        """Load control mappings from YAML files."""
        for path in paths:
            content = path.read_text()
            data = yaml.safe_load(content)
            
            mappings = data if isinstance(data, list) else [data]
            
            for map_data in mappings:
                mapping = ControlMapping(
                    id=map_data.get("id", ""),
                    control_id=map_data.get("control_id", ""),
                    requirement_id=map_data.get("requirement_id", ""),
                    strength=map_data.get("strength", "full"),
                    reviewer_note=map_data.get("reviewer_note", ""),
                )
                self.mappings.append(mapping)

    def get_control(self, control_id: str) -> Control | None:
        """Get a control by ID."""
        return self.controls.get(control_id)

    def get_requirement(self, requirement_id: str) -> Requirement | None:
        """Get a requirement by ID."""
        return self.requirements.get(requirement_id)

    def get_mappings_for_control(self, control_id: str) -> list[ControlMapping]:
        """Get all mappings for a control."""
        return [m for m in self.mappings if m.control_id == control_id]

    def get_mappings_for_requirement(self, requirement_id: str) -> list[ControlMapping]:
        """Get all mappings for a requirement."""
        return [m for m in self.mappings if m.requirement_id == requirement_id]
