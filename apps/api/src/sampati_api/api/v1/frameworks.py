# SPDX-License-Identifier: Apache-2.0
"""Framework API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ....auth.dependencies import get_current_user, require_role
from ....database import get_tenant_session
from ....services.framework_service import FrameworkService

router = APIRouter(prefix="/frameworks", tags=["frameworks"])


class FrameworkLoadRequest(BaseModel):
    file_path: str = Field(..., description="Path to framework YAML/JSON file")


class FrameworkResponse(BaseModel):
    id: str
    code: str
    name: str
    version: str
    status: str
    description: str
    source_url: str | None
    requirements_count: int


class EntityFrameworkSelect(BaseModel):
    framework_id: str
    framework_version_id: str


class FrameworkProgressResponse(BaseModel):
    framework_id: str
    framework_name: str
    total_requirements: int
    implemented_requirements: int
    partial_requirements: int
    not_started_requirements: int
    not_applicable_requirements: int
    readiness_score: float


class GapItem(BaseModel):
    requirement_id: str
    requirement_reference: str
    requirement_title: str
    status: str
    mapped_controls: list[dict]
    gap_severity: str


@router.post("/load", response_model=FrameworkResponse, status_code=status.HTTP_201_CREATED)
async def load_framework(
    request: FrameworkLoadRequest,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> FrameworkResponse:
    """Load a framework from a file (admin/compliance_manager only)."""
    service = FrameworkService()
    framework = await service.load_framework(request.file_path)
    
    return FrameworkResponse(
        id=framework.id,
        code=framework.code,
        name=framework.name,
        version=framework.version,
        status=framework.status.value,
        description=framework.description,
        source_url=framework.source_url,
        requirements_count=len(service.get_requirements_for_framework(framework.id)),
    )


@router.get("", response_model=list[FrameworkResponse])
async def list_frameworks(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[FrameworkResponse]:
    """List loaded frameworks."""
    service = FrameworkService()
    frameworks = service.list_frameworks()
    
    return [
        FrameworkResponse(
            id=f.id,
            code=f.code,
            name=f.name,
            version=f.version,
            status=f.status.value,
            description=f.description,
            source_url=f.source_url,
            requirements_count=len(service.get_requirements_for_framework(f.id)),
        )
        for f in frameworks
    ]


@router.get("/{framework_id}", response_model=FrameworkResponse)
async def get_framework(
    framework_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> FrameworkResponse:
    """Get a framework by ID."""
    service = FrameworkService()
    framework = service.get_framework(framework_id)
    
    if not framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Framework not found",
        )
    
    return FrameworkResponse(
        id=framework.id,
        code=framework.code,
        name=framework.name,
        version=framework.version,
        status=framework.status.value,
        description=framework.description,
        source_url=framework.source_url,
        requirements_count=len(service.get_requirements_for_framework(framework.id)),
    )


@router.post("/entities/{entity_id}/frameworks", status_code=status.HTTP_201_CREATED)
async def select_framework_for_entity(
    entity_id: str,
    request: EntityFrameworkSelect,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> dict[str, str]:
    """Select a framework for an entity."""
    service = FrameworkService()
    await service.select_framework_for_entity(
        entity_id=entity_id,
        framework_id=request.framework_id,
        framework_version_id=request.framework_version_id,
    )
    return {"message": "Framework selected for entity"}


@router.get("/entities/{entity_id}/frameworks", response_model=list[FrameworkProgressResponse])
async def get_entity_frameworks_progress(
    entity_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[FrameworkProgressResponse]:
    """Get framework progress for an entity."""
    service = FrameworkService()
    progress_list = await service.get_entity_framework_progress(entity_id)
    
    return [
        FrameworkProgressResponse(
            framework_id=p.framework_id,
            framework_name=p.framework_name,
            total_requirements=p.total_requirements,
            implemented_requirements=p.implemented_requirements,
            partial_requirements=p.partial_requirements,
            not_started_requirements=p.not_started_requirements,
            not_applicable_requirements=p.not_applicable_requirements,
            readiness_score=p.readiness_score,
        )
        for p in progress_list
    ]


@router.get("/entities/{entity_id}/gap-analysis", response_model=list[GapItem])
async def get_gap_analysis(
    entity_id: str,
    framework_id: Annotated[str, Query()],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[GapItem]:
    """Get gap analysis for an entity against a framework."""
    service = FrameworkService()
    gaps = await service.get_gap_analysis(entity_id, framework_id)
    
    return [
        GapItem(
            requirement_id=g["requirement_id"],
            requirement_reference=g["requirement_reference"],
            requirement_title=g["requirement_title"],
            status=g["status"],
            mapped_controls=g["mapped_controls"],
            gap_severity=g["gap_severity"],
        )
        for g in gaps
    ]
