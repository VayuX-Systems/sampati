# SPDX-License-Identifier: Apache-2.0
"""Framework service for loading and managing frameworks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sampati_core_domain.framework import FrameworkLoader, CrosswalkEngine
from sampati_core_domain.framework.models import Framework, Requirement, Control, ControlMapping, ControlImplementation, ControlStatus
from sampati_core_domain.models import EntityFramework


class FrameworkService:
    """Service for managing frameworks, controls, and crosswalks."""

    def __init__(self) -> None:
        self.loader = FrameworkLoader()
        self.crosswalk = CrosswalkEngine()

    def load_framework(self, file_path: str) -> Framework:
        """Load a framework from a file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Framework file not found: {file_path}")
        
        framework = self.loader.load_framework_file(path)
        
        # Register with crosswalk engine
        self.crosswalk.register_control = lambda c: None  # Controls loaded separately
        # Note: In production, we'd persist to database
        
        return framework

    def load_controls(self, paths: list[str]) -> None:
        """Load controls from files."""
        path_objs = [Path(p) for p in paths]
        self.loader.load_controls(path_objs)
        
        # Register with crosswalk
        for control in self.loader.controls.values():
            self.crosswalk.register_control(control)

    def load_mappings(self, paths: list[str]) -> None:
        """Load control mappings from files."""
        path_objs = [Path(p) for p in paths]
        self.loader.load_mappings(path_objs)
        
        # Register with crosswalk
        for mapping in self.loader.mappings:
            self.crosswalk.register_mapping(mapping)

    def list_frameworks(self) -> list[Framework]:
        """List all loaded frameworks."""
        return list(self.loader.frameworks.values())

    def get_framework(self, framework_id: str) -> Framework | None:
        """Get a framework by ID."""
        return self.loader.frameworks.get(framework_id)

    def get_requirements_for_framework(self, framework_id: str) -> list[Requirement]:
        """Get all requirements for a framework."""
        # In production, this would query by framework_version_id
        return list(self.loader.requirements.values())

    async def select_framework_for_entity(
        self,
        entity_id: str,
        framework_id: str,
        framework_version_id: str,
    ) -> None:
        """Select a framework for an entity."""
        # In production, this would create an EntityFramework record in the database
        # For now, we just note the selection
        pass

    async def get_entity_framework_progress(self, entity_id: str) -> list[Any]:
        """Get framework progress for an entity."""
        # In production, this would query EntityFramework records and calculate progress
        # For now, return empty list
        return []

    async def get_gap_analysis(self, entity_id: str, framework_id: str) -> list[dict[str, Any]]:
        """Get gap analysis for an entity against a framework."""
        # In production, this would:
        # 1. Get framework requirements
        # 2. Get entity's control implementations
        # 3. Use crosswalk engine to calculate gaps
        return []
