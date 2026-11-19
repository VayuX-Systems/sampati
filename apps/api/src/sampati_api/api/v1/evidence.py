# SPDX-License-Identifier: Apache-2.0
"""Evidence API routes."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ....auth.dependencies import get_current_user, require_role
from ....database import get_tenant_session
from ....services.evidence_service import EvidenceService

router = APIRouter(prefix="/evidence", tags=["evidence"])


class EvidenceCreate(BaseModel):
    source_plugin: str = Field(..., min_length=1)
    plugin_version: str = Field(..., min_length=1)
    collector: str = Field(..., pattern="^(connector|agent|manual|scanner)$")
    check: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    result: str = Field(..., pattern="^(pass|fail|error|info)$")
    data: dict = Field(default_factory=dict)
    valid_until_days: int | None = Field(None, ge=1, le=3650)
    linked_controls: list[str] = Field(default_factory=list)


class EvidenceResponse(BaseModel):
    id: str
    organisation_id: str
    source_plugin: str
    plugin_version: str
    collector: str
    check: str
    subject: str
    result: str
    collected_at: str
    valid_until: str | None
    data: dict
    hash: str
    prev_hash: str
    linked_controls: list[str]


class EvidenceVerifyResponse(BaseModel):
    valid: bool
    errors: list[str] = []


@router.post("", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def create_evidence(
    evidence: EvidenceCreate,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager", "control_owner", "contributor"))],
) -> EvidenceResponse:
    """Create a new evidence record (manual or automated)."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        record = await service.create_evidence(
            organisation_id=current_user["organisation_id"],
            source_plugin=evidence.source_plugin,
            plugin_version=evidence.plugin_version,
            collector=evidence.collector,
            check=evidence.check,
            subject=evidence.subject,
            result=evidence.result,
            data=evidence.data,
            valid_until_days=evidence.valid_until_days,
            linked_controls=evidence.linked_controls,
        )
        
        return EvidenceResponse(
            id=record.id,
            organisation_id=record.organisation_id,
            source_plugin=record.source_plugin,
            plugin_version=record.plugin_version,
            collector=record.collector.value,
            check=record.check,
            subject=record.subject,
            result=record.result.value,
            collected_at=record.collected_at.isoformat(),
            valid_until=record.valid_until.isoformat() if record.valid_until else None,
            data=record.data,
            hash=record.hash,
            prev_hash=record.prev_hash,
            linked_controls=record.linked_controls,
        )


@router.get("", response_model=list[EvidenceResponse])
async def list_evidence(
    current_user: Annotated[dict, Depends(get_current_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    check: Annotated[Optional[str], Query()] = None,
    result: Annotated[Optional[str], Query()] = None,
    since: Annotated[Optional[str], Query()] = None,
) -> list[EvidenceResponse]:
    """List evidence records with optional filters."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        records = await service.list_evidence(
            organisation_id=current_user["organisation_id"],
            limit=limit,
            offset=offset,
            check=check,
            result=result,
            since=since,
        )
        
        return [
            EvidenceResponse(
                id=r.id,
                organisation_id=r.organisation_id,
                source_plugin=r.source_plugin,
                plugin_version=r.plugin_version,
                collector=r.collector.value,
                check=r.check,
                subject=r.subject,
                result=r.result.value,
                collected_at=r.collected_at.isoformat(),
                valid_until=r.valid_until.isoformat() if r.valid_until else None,
                data=r.data,
                hash=r.hash,
                prev_hash=r.prev_hash,
                linked_controls=r.linked_controls,
            )
            for r in records
        ]


@router.get("/verify", response_model=EvidenceVerifyResponse)
async def verify_ledger(
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager", "auditor"))],
) -> EvidenceVerifyResponse:
    """Verify the integrity of the evidence ledger hash chain."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        is_valid, errors = await service.verify_chain(current_user["organisation_id"])
        return EvidenceVerifyResponse(valid=is_valid, errors=errors)


@router.get("/latest-hash")
async def get_latest_hash(
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager", "auditor"))],
) -> dict[str, str]:
    """Get the latest hash in the chain."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        hash_val = await service.get_latest_hash(current_user["organisation_id"])
        return {"hash": hash_val}


@router.get("/stale")
async def get_stale_evidence(
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
    threshold_days: Annotated[int, Query(ge=1, le=365)] = 90,
) -> list[EvidenceResponse]:
    """Get evidence records that have expired."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        records = await service.get_stale_evidence(current_user["organisation_id"], threshold_days)
        
        return [
            EvidenceResponse(
                id=r.id,
                organisation_id=r.organisation_id,
                source_plugin=r.source_plugin,
                plugin_version=r.plugin_version,
                collector=r.collector.value,
                check=r.check,
                subject=r.subject,
                result=r.result.value,
                collected_at=r.collected_at.isoformat(),
                valid_until=r.valid_until.isoformat() if r.valid_until else None,
                data=r.data,
                hash=r.hash,
                prev_hash=r.prev_hash,
                linked_controls=r.linked_controls,
            )
            for r in records
        ]


@router.get("/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(
    evidence_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EvidenceResponse:
    """Get a single evidence record by ID."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceService(session)
        record = await service.get_evidence(evidence_id, current_user["organisation_id"])
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evidence record not found",
            )
        
        return EvidenceResponse(
            id=record.id,
            organisation_id=record.organisation_id,
            source_plugin=record.source_plugin,
            plugin_version=record.plugin_version,
            collector=record.collector.value,
            check=record.check,
            subject=record.subject,
            result=record.result.value,
            collected_at=record.collected_at.isoformat(),
            valid_until=record.valid_until.isoformat() if record.valid_until else None,
            data=record.data,
            hash=record.hash,
            prev_hash=record.prev_hash,
            linked_controls=record.linked_controls,
        )
