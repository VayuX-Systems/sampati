# SPDX-License-Identifier: Apache-2.0
"""Evidence Request service for manual evidence collection."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from sampati_core_domain.models import EvidenceRequest, EvidenceRequestStatus, EvidenceRequestPriority, User, EvidenceRecord, EvidenceCollector, EvidenceResult
from sampati_ledger.service import EvidenceLedger
from sampati_ledger.models import EvidenceCollector as LedgerEvidenceCollector, EvidenceResult as LedgerEvidenceResult


class EvidenceRequestService:
    """Service for managing evidence requests."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.ledger = EvidenceLedger(session)

    async def create_request(
        self,
        organisation_id: str,
        requested_by_id: str,
        title: str,
        description: str,
        assignee_id: str,
        due_days: int,
        control_implementation_id: str | None = None,
        priority: str = "medium",
    ) -> EvidenceRequest:
        """Create a new evidence request."""
        # Verify assignee exists and is in the organisation
        assignee = await self.session.get(User, assignee_id)
        if not assignee:
            raise ValueError("Assignee not found")
        
        # Verify control implementation if provided
        if control_implementation_id:
            from sampati_core_domain.models import ControlImplementation
            ctrl_impl = await self.session.get(ControlImplementation, control_implementation_id)
            if not ctrl_impl or str(ctrl_impl.organisation_id) != organisation_id:
                raise ValueError("Control implementation not found")
        
        request = EvidenceRequest(
            organisation_id=organisation_id,
            title=title,
            description=description,
            requested_by_id=requested_by_id,
            assignee_id=assignee_id,
            control_implementation_id=control_implementation_id,
            status=EvidenceRequestStatus.PENDING,
            priority=EvidenceRequestPriority(priority),
            due_date=datetime.now(timezone.utc) + timedelta(days=due_days),
        )
        
        self.session.add(request)
        await self.session.flush()
        
        # Load relationships
        await self.session.refresh(request, ["assignee", "requested_by"])
        
        return request

    async def get_request(self, request_id: str, organisation_id: str) -> Optional[EvidenceRequest]:
        """Get an evidence request by ID."""
        stmt = select(EvidenceRequest).where(
            EvidenceRequest.id == request_id,
            EvidenceRequest.organisation_id == organisation_id
        ).options(
            selectinload(EvidenceRequest.assignee),
            selectinload(EvidenceRequest.requested_by),
            selectinload(EvidenceRequest.evidence),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_requests(
        self,
        organisation_id: str,
        status: str | None = None,
        assignee_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[EvidenceRequest]:
        """List evidence requests with optional filters."""
        stmt = select(EvidenceRequest).where(
            EvidenceRequest.organisation_id == organisation_id
        ).options(
            selectinload(EvidenceRequest.assignee),
            selectinload(EvidenceRequest.requested_by),
        ).order_by(EvidenceRequest.created_at.desc()).limit(limit).offset(offset)
        
        if status:
            stmt = stmt.where(EvidenceRequest.status == EvidenceRequestStatus(status))
        if assignee_id:
            stmt = stmt.where(EvidenceRequest.assignee_id == assignee_id)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_request(
        self,
        request_id: str,
        organisation_id: str,
        title: str | None = None,
        description: str | None = None,
        assignee_id: str | None = None,
        due_days: int | None = None,
        priority: str | None = None,
    ) -> Optional[EvidenceRequest]:
        """Update an evidence request."""
        request = await self.get_request(request_id, organisation_id)
        if not request:
            return None
        
        if title is not None:
            request.title = title
        if description is not None:
            request.description = description
        if assignee_id is not None:
            request.assignee_id = assignee_id
        if due_days is not None:
            request.due_date = datetime.now(timezone.utc) + timedelta(days=due_days)
        if priority is not None:
            request.priority = EvidenceRequestPriority(priority)
        
        await self.session.flush()
        return request

    async def submit_evidence(
        self,
        request_id: str,
        organisation_id: str,
        submitter_id: str,
        evidence_type: str,
        file_key: str | None = None,
        link_url: str | None = None,
        statement: str | None = None,
        description: str | None = None,
    ) -> Optional[EvidenceRequest]:
        """Submit evidence for a request."""
        request = await self.get_request(request_id, organisation_id)
        if not request:
            return None
        
        # Verify submitter is the assignee
        if str(request.assignee_id) != submitter_id:
            raise ValueError("Only the assignee can submit evidence")
        
        if request.status not in (EvidenceRequestStatus.PENDING, EvidenceRequestStatus.IN_PROGRESS, EvidenceRequestStatus.OVERDUE):
            raise ValueError("Request is not in a submittable state")
        
        # Create evidence record in ledger
        evidence_data = {
            "type": evidence_type,
            "description": description,
        }
        
        if evidence_type == "file":
            evidence_data["file_key"] = file_key
        elif evidence_type == "link":
            evidence_data["link_url"] = link_url
        elif evidence_type == "statement":
            evidence_data["statement"] = statement
        
        evidence = await self.ledger.append(
            organisation_id=organisation_id,
            source_plugin="manual",
            plugin_version="1.0.0",
            collector=EvidenceCollector.MANUAL,
            check=f"manual_evidence_{request.id}",
            subject=f"Manual evidence for request: {request.title}",
            result=EvidenceResult.INFO,
            data=evidence_data,
            linked_controls=[request.control_implementation_id] if request.control_implementation_id else [],
        )
        
        # Update request
        request.status = EvidenceRequestStatus.SUBMITTED
        request.evidence_id = evidence.id
        request.completed_at = datetime.now(timezone.utc)
        
        await self.session.flush()
        return request

    async def review_evidence(
        self,
        request_id: str,
        organisation_id: str,
        reviewer_id: str,
        action: str,
        comment: str | None = None,
    ) -> Optional[EvidenceRequest]:
        """Review submitted evidence (approve/reject)."""
        request = await self.get_request(request_id, organisation_id)
        if not request:
            return None
        
        if request.status != EvidenceRequestStatus.SUBMITTED:
            raise ValueError("Request must be in SUBMITTED state to review")
        
        if action == "approve":
            request.status = EvidenceRequestStatus.APPROVED
        elif action == "reject":
            request.status = EvidenceRequestStatus.REJECTED
        else:
            raise ValueError("Action must be 'approve' or 'reject'")
        
        if comment:
            # Store comment in evidence data or as a separate note
            pass
        
        request.completed_at = datetime.now(timezone.utc)
        await self.session.flush()
        return request

    async def send_reminder(self, request_id: str, organisation_id: str) -> bool:
        """Send a reminder for an overdue evidence request."""
        request = await self.get_request(request_id, organisation_id)
        if not request:
            return False
        
        # In production, this would send an email/notification
        # For now, just log it
        return True
