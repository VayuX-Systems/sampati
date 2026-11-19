# SPDX-License-Identifier: Apache-2.0
"""Crosswalk engine for 'implement once, comply many'."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .models import Control, ControlMapping, ControlImplementation, ControlStatus, Requirement


@dataclass
class FrameworkProgress:
    """Progress of a framework for an entity."""
    framework_id: str
    framework_name: str
    total_requirements: int = 0
    implemented_requirements: int = 0
    partial_requirements: int = 0
    not_started_requirements: int = 0
    not_applicable_requirements: int = 0
    
    @property
    def readiness_score(self) -> float:
        """Calculate readiness score (0-100)."""
        if self.total_requirements == 0:
            return 0.0
        # Full credit for implemented, half for partial
        score = (self.implemented_requirements + 0.5 * self.partial_requirements) / self.total_requirements
        return round(score * 100, 1)


class CrosswalkEngine:
    """
    Crosswalk engine that maps controls to framework requirements.
    
    Implements the 'implement once, comply many' principle.
    """

    def __init__(self) -> None:
        self.controls: dict[str, Control] = {}
        self.requirements: dict[str, Requirement] = {}
        self.mappings: list[ControlMapping] = []
        self.implementations: dict[str, ControlImplementation] = {}
        
        # Indexes for fast lookups
        self._mappings_by_control: dict[str, list[ControlMapping]] = defaultdict(list)
        self._mappings_by_requirement: dict[str, list[ControlMapping]] = defaultdict(list)

    def register_control(self, control: Control) -> None:
        """Register a control."""
        self.controls[control.id] = control

    def register_requirement(self, requirement: Requirement) -> None:
        """Register a framework requirement."""
        self.requirements[requirement.id] = requirement

    def register_mapping(self, mapping: ControlMapping) -> None:
        """Register a control-to-requirement mapping."""
        self.mappings.append(mapping)
        self._mappings_by_control[mapping.control_id].append(mapping)
        self._mappings_by_requirement[mapping.requirement_id].append(mapping)

    def register_implementation(self, implementation: ControlImplementation) -> None:
        """Register a control implementation."""
        self.implementations[implementation.id] = implementation

    def get_requirements_for_control(self, control_id: str) -> list[Requirement]:
        """Get all requirements that a control maps to."""
        mappings = self._mappings_by_control.get(control_id, [])
        return [self.requirements[m.requirement_id] for m in mappings if m.requirement_id in self.requirements]

    def get_controls_for_requirement(self, requirement_id: str) -> list[Control]:
        """Get all controls that map to a requirement."""
        mappings = self._mappings_by_requirement.get(requirement_id, [])
        return [self.controls[m.control_id] for m in mappings if m.control_id in self.controls]

    def calculate_framework_progress(self, entity_id: str, framework_requirements: list[Requirement]) -> FrameworkProgress:
        """Calculate progress for a framework for a given entity."""
        progress = FrameworkProgress(
            framework_id="",
            framework_name="",
            total_requirements=len(framework_requirements),
        )
        
        # Find implementations for this entity
        entity_implementations = {
            impl.control_id: impl 
            for impl in self.implementations.values() 
            if impl.entity_id == entity_id
        }
        
        for req in framework_requirements:
            mapped_controls = self.get_controls_for_requirement(req.id)
            
            if not mapped_controls:
                progress.not_started_requirements += 1
                continue
            
            # Check implementation status of mapped controls
            statuses = []
            for control in mapped_controls:
                impl = entity_implementations.get(control.id)
                if impl:
                    statuses.append(impl.status)
                else:
                    statuses.append(ControlStatus.NOT_STARTED)
            
            # Determine requirement status based on control statuses
            if any(s == ControlStatus.NOT_APPLICABLE for s in statuses):
                # If any mapped control is N/A with reason, requirement is N/A
                progress.not_applicable_requirements += 1
            elif all(s == ControlStatus.IMPLEMENTED for s in statuses):
                progress.implemented_requirements += 1
            elif any(s == ControlStatus.IMPLEMENTED for s in statuses) or any(s == ControlStatus.IN_PROGRESS for s in statuses):
                progress.partial_requirements += 1
            else:
                progress.not_started_requirements += 1
        
        return progress

    def get_gap_analysis(self, entity_id: str, framework_requirements: list[Requirement]) -> list[dict[str, Any]]:
        """Get prioritized gap list for a framework."""
        gaps = []
        entity_implementations = {
            impl.control_id: impl 
            for impl in self.implementations.values() 
            if impl.entity_id == entity_id
        }
        
        for req in framework_requirements:
            mapped_controls = self.get_controls_for_requirement(req.id)
            
            if not mapped_controls:
                gaps.append({
                    "requirement_id": req.id,
                    "requirement_reference": req.reference,
                    "requirement_title": req.title,
                    "status": "not_mapped",
                    "mapped_controls": [],
                    "gap_severity": "high",
                })
                continue
            
            # Find worst status among mapped controls
            statuses = []
            control_details = []
            for control in mapped_controls:
                impl = entity_implementations.get(control.id)
                if impl:
                    statuses.append(impl.status)
                    control_details.append({
                        "control_id": control.id,
                        "control_code": control.code,
                        "status": impl.status.value,
                        "owner_id": impl.owner_id,
                    })
                else:
                    statuses.append(ControlStatus.NOT_STARTED)
                    control_details.append({
                        "control_id": control.id,
                        "control_code": control.code,
                        "status": "not_started",
                        "owner_id": None,
                    })
            
            # Determine overall requirement status
            if any(s == ControlStatus.NOT_APPLICABLE for s in statuses):
                req_status = "not_applicable"
                severity = "none"
            elif all(s == ControlStatus.IMPLEMENTED for s in statuses):
                req_status = "implemented"
                severity = "none"
            elif any(s == ControlStatus.IMPLEMENTED for s in statuses) or any(s == ControlStatus.IN_PROGRESS for s in statuses):
                req_status = "partial"
                severity = "medium"
            else:
                req_status = "not_started"
                severity = "high"
            
            if req_status != "implemented" and req_status != "not_applicable":
                gaps.append({
                    "requirement_id": req.id,
                    "requirement_reference": req.reference,
                    "requirement_title": req.title,
                    "status": req_status,
                    "mapped_controls": control_details,
                    "gap_severity": severity,
                })
        
        # Sort by severity (high first) then by reference
        severity_order = {"high": 0, "medium": 1, "low": 2, "none": 3}
        gaps.sort(key=lambda g: (severity_order.get(g["gap_severity"], 3), g["requirement_reference"]))
        
        return gaps
