# SPDX-License-Identifier: Apache-2.0
"""Organisation API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ....auth.dependencies import get_current_user, require_role
from ....database import get_tenant_session
from ....models import Organisation, Entity

router = APIRouter(prefix="/organisations", tags=["organisations"])


class OrganisationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=64, pattern="^[a-z0-9-]+$")
    region: str = Field(default="IN", pattern="^[A-Z]{2}$")


class OrganisationUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    region: str | None = Field(None, pattern="^[A-Z]{2}$")
    status: str | None = Field(None, pattern="^(active|archived)$")


class OrganisationResponse(BaseModel):
    id: str
    name: str
    slug: str
    region: str
    status: str
    settings: dict
    created_at: str
    updated_at: str


class EntityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(default="legal_entity", pattern="^(legal_entity|business_unit)$")
    parent_entity_id: str | None = None


class EntityResponse(BaseModel):
    id: str
    name: str
    type: str
    parent_entity_id: str | None
    created_at: str
    updated_at: str


@router.post("", response_model=OrganisationResponse, status_code=status.HTTP_201_CREATED)
async def create_organisation(
    org: OrganisationCreate,
    current_user: Annotated[dict, Depends(require_role("admin"))],
) -> OrganisationResponse:
    """Create a new organisation (admin only)."""
    async with get_tenant_session(current_user.organisation_id) as session:
        # Check if slug exists
        from sqlalchemy import select
        result = await session.execute(
            select(Organisation).where(Organisation.slug == org.slug)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organisation slug already exists",
            )
        
        new_org = Organisation(
            name=org.name,
            slug=org.slug,
            region=org.region,
        )
        session.add(new_org)
        await session.flush()
        
        # Create admin membership for current user
        from ....models import Membership
        membership = Membership(
            user_id=current_user.user_id,
            organisation_id=new_org.id,
            role="admin",
        )
        session.add(membership)
        
        return OrganisationResponse(
            id=str(new_org.id),
            name=new_org.name,
            slug=new_org.slug,
            region=new_org.region,
            status=new_org.status.value,
            settings=new_org.settings,
            created_at=new_org.created_at.isoformat(),
            updated_at=new_org.updated_at.isoformat(),
        )


@router.get("/{org_id}", response_model=OrganisationResponse)
async def get_organisation(
    org_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> OrganisationResponse:
    """Get an organisation by ID."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Organisation).where(Organisation.id == org_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organisation not found",
            )
        
        return OrganisationResponse(
            id=str(org.id),
            name=org.name,
            slug=org.slug,
            region=org.region,
            status=org.status.value,
            settings=org.settings,
            created_at=org.created_at.isoformat(),
            updated_at=org.updated_at.isoformat(),
        )


@router.patch("/{org_id}", response_model=OrganisationResponse)
async def update_organisation(
    org_id: str,
    update: OrganisationUpdate,
    current_user: Annotated[dict, Depends(require_role("admin"))],
) -> OrganisationResponse:
    """Update an organisation."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Organisation).where(Organisation.id == org_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organisation not found",
            )
        
        if update.name is not None:
            org.name = update.name
        if update.region is not None:
            org.region = update.region
        if update.status is not None:
            org.status = update.status
        
        await session.flush()
        
        return OrganisationResponse(
            id=str(org.id),
            name=org.name,
            slug=org.slug,
            region=org.region,
            status=org.status.value,
            settings=org.settings,
            created_at=org.created_at.isoformat(),
            updated_at=org.updated_at.isoformat(),
        )


@router.get("", response_model=list[OrganisationResponse])
async def list_organisations(
    current_user: Annotated[dict, Depends(get_current_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Query()] = None,
) -> list[OrganisationResponse]:
    """List organisations user has access to."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        query = select(Organisation).limit(limit)
        if cursor:
            query = query.where(Organisation.id > cursor)
        
        result = await session.execute(query)
        orgs = result.scalars().all()
        
        return [
            OrganisationResponse(
                id=str(o.id),
                name=o.name,
                slug=o.slug,
                region=o.region,
                status=o.status.value,
                settings=o.settings,
                created_at=o.created_at.isoformat(),
                updated_at=o.updated_at.isoformat(),
            )
            for o in orgs
        ]


@router.post("/{org_id}/entities", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
async def create_entity(
    org_id: str,
    entity: EntityCreate,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> EntityResponse:
    """Create an entity within an organisation."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        from ....models import EntityType
        
        # Verify organisation exists
        result = await session.execute(
            select(Organisation).where(Organisation.id == org_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organisation not found",
            )
        
        new_entity = Entity(
            organisation_id=org_id,
            name=entity.name,
            type=EntityType(entity.type),
            parent_entity_id=entity.parent_entity_id,
        )
        session.add(new_entity)
        await session.flush()
        
        return EntityResponse(
            id=str(new_entity.id),
            name=new_entity.name,
            type=new_entity.type.value,
            parent_entity_id=str(new_entity.parent_entity_id) if new_entity.parent_entity_id else None,
            created_at=new_entity.created_at.isoformat(),
            updated_at=new_entity.updated_at.isoformat(),
        )


@router.get("/{org_id}/entities", response_model=list[EntityResponse])
async def list_entities(
    org_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[EntityResponse]:
    """List entities in an organisation."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Entity).where(Entity.organisation_id == org_id).order_by(Entity.name)
        )
        entities = result.scalars().all()
        
        return [
            EntityResponse(
                id=str(e.id),
                name=e.name,
                type=e.type.value,
                parent_entity_id=str(e.parent_entity_id) if e.parent_entity_id else None,
                created_at=e.created_at.isoformat(),
                updated_at=e.updated_at.isoformat(),
            )
            for e in entities
        ]
