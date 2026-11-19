# SPDX-License-Identifier: Apache-2.0
"""Evidence Requests API routes - for manual evidence collection."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ....auth.dependencies import get_current_user, require_role
from ....database import get_tenant_session
from ....models import EvidenceRequest, EvidenceRequestStatus, User
from ....services.evidence_request_service import EvidenceRequestService

router = APIRouter(prefix="/evidence-requests", tags=["evidence-requests"])


class EvidenceRequestCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    assignee_id: str = Field(..., description="User ID to assign the request to")
    due_days: int = Field(default=14, ge=1, le=365)
    control_implementation_id: str | None = Field(None, description="Link to control implementation")
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")


class EvidenceRequestUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    assignee_id: str | None = None
    due_days: int | None = Field(None, ge=1, le=365)
    priority: str | None = Field(None, pattern="^(low|medium|high|critical)$")


class EvidenceRequestResponse(BaseModel):
    id: str
    organisation_id: str
    title: str
    description: str
    assignee_id: str
    assignee_name: str
    assignee_email: str
    requested_by_id: str
    requested_by_name: str
    status: str
    priority: str
    due_date: str
    control_implementation_id: str | None
    created_at: str
    updated_at: str
    completed_at: str | None
    evidence_id: str | None


class EvidenceSubmission(BaseModel):
    evidence_type: str = Field(..., pattern="^(file|link|statement)$")
    file_key: str | None = None
    link_url: str | None = None
    statement: str | None = None
    description: str | None = None


class EvidenceReview(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
    comment: str | None = None


@router.post("", response_model=EvidenceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_evidence_request(
    request: EvidenceRequestCreate,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager", "control_owner"))],
) -> EvidenceRequestResponse:
    """Create a new evidence request (for manual evidence collection)."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        evidence_request = await service.create_request(
            organisation_id=current_user["organisation_id"],
            requested_by_id=current_user["user_id"],
            title=request.title,
            description=request.description,
            assignee_id=request.assignee_id,
            due_days=request.due_days,
            control_implementation_id=request.control_implementation_id,
            priority=request.priority,
        )
        return _to_response(evidence_request)


@router.get("", response_model=list[EvidenceRequestResponse])
async def list_evidence_requests(
    current_user: Annotated[dict, Depends(get_current_user)],
    status: Annotated[Optional[str], Query()] = None,
    assignee_id: Annotated[Optional[str], Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[EvidenceRequestResponse]:
    """List evidence requests with optional filters."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        
        # If user is not admin/compliance_manager, only show their requests
        if current_user["roles"] not in ("admin", "compliance_manager"):
            assignee_id = current_user["user_id"]
        
        requests = await service.list_requests(
            organisation_id=current_user["organisation_id"],
            status=status,
            assignee_id=assignee_id,
            limit=limit,
            offset=offset,
        )
        return [_to_response(r) for r in requests]


@router.get("/{request_id}", response_model=EvidenceRequestResponse)
async def get_evidence_request(
    request_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EvidenceRequestResponse:
    """Get an evidence request by ID."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        evidence_request = await service.get_request(request_id, current_user["organisation_id"])
        
        if not evidence_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evidence request not found",
            )
        
        # Check permissions
        if (current_user["roles"] not in ("admin", "compliance_manager") and 
            evidence_request.assignee_id != current_user["user_id"] and
            evidence_request.requested_by_id != current_user["user_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this request",
            )
        
        return _to_response(evidence_request)


@router.patch("/{request_id}", response_model=EvidenceRequestResponse)
async def update_evidence_request(
    request_id: str,
    update: EvidenceRequestUpdate,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> EvidenceRequestResponse:
    """Update an evidence request."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        evidence_request = await service.update_request(
            request_id=request_id,
            organisation_id=current_user["organisation_id"],
            title=update.title,
            description=update.description,
            assignee_id=update.assignee_id,
            due_days=update.due_days,
            priority=update.priority,
        )
        
        if not evidence_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evidence request not found",
            )
        
        return _to_response(evidence_request)


@router.post("/{request_id}/submit", response_model=EvidenceRequestResponse)
async def submit_evidence(
    request_id: str,
    submission: EvidenceSubmission,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EvidenceRequestResponse:
    """Submit evidence for a request (by assignee)."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        evidence_request = await service.submit_evidence(
            request_id=request_id,
            organisation_id=current_user["organisation_id"],
            submitter_id=current_user["user_id"],
            evidence_type=submission.evidence_type,
            file_key=submission.file_key,
            link_url=submission.link_url,
            statement=submission.statement,
            description=submission.description,
        )
        
        if not evidence_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evidence request not found",
            )
        
        return _to_response(evidence_request)


@router.post("/{request_id}/review", response_model=EvidenceRequestResponse)
async def review_evidence(
    request_id: str,
    review: EvidenceReview,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> EvidenceRequestResponse:
    """Review submitted evidence (approve/reject)."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        evidence_request = await service.review_evidence(
            request_id=request_id,
            organisation_id=current_user["organisation_id"],
            reviewer_id=current_user["user_id"],
            action=review.action,
            comment=review.comment,
        )
        
        if not evidence_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evidence request not found",
            )
        
        return _to_response(evidence_request)


@router.post("/{request_id}/remind")
async def send_reminder(
    request_id: str,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager", "control_owner"))],
) -> dict[str, str]:
    """Send a reminder for an overdue evidence request."""
    async with get_tenant_session(current_user["organisation_id"]) as session:
        service = EvidenceRequestService(session)
        await service.send_reminder(request_id, current_user["organisation_id"])
        return {"message": "Reminder sent"}


def _to_response(request) -> EvidenceRequestResponse:
    """Convert EvidenceRequest model to response."""
    return EvidenceRequestResponse(
        id=str(request.id),
        organisation_id=str(request.organisation_id),
        title=request.title,
        description=request.description,
        assignee_id=str(request.assignee_id),
        assignee_name=request.assignee.name if request.assignee else "",
        assignee_email=request.assignee.email if request.assignee else "",
        requested_by_id=str(request.requested_by_id),
        requested_by_name=request.requested_by.name if request.requested_by else "",
        status=request.status.value,
        priority=request.priority,
        due_date=request.due_date.isoformat(),
        control_implementation_id=str(request.control_implementation_id) if request.control_implementation_id else None,
        created_at=request.created_at.isoformat(),
        updated_at=request.updated_at.isoformat(),
        completed_at=request.completed_at.isoformat() if request.completed_at else None,
        evidence_id=str(request.evidence_id) if request.evidence_id else None,
    )
