# SPDX-License-Identifier: Apache-2.0
"""Evidence Request model for manual evidence collection."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, OrganisationMixin, TimestampMixin, generate_uuid7

if TYPE_CHECKING:
    from .user import User
    from .evidence import EvidenceRecord


class EvidenceRequestStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class EvidenceRequestPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvidenceRequest(Base, TimestampMixin, OrganisationMixin):
    """Request for manual evidence collection."""

    __tablename__ = "evidence_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requested_by_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    assignee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    control_implementation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("control_implementations.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[EvidenceRequestStatus] = mapped_column(
        Enum(EvidenceRequestStatus),
        default=EvidenceRequestStatus.PENDING,
        nullable=False,
    )
    priority: Mapped[EvidenceRequestPriority] = mapped_column(
        Enum(EvidenceRequestPriority),
        default=EvidenceRequestPriority.MEDIUM,
        nullable=False,
    )
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    evidence_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("evidence_records.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    requested_by: Mapped["User"] = relationship(foreign_keys=[requested_by_id])
    assignee: Mapped["User"] = relationship(foreign_keys=[assignee_id])
    control_implementation: Mapped["ControlImplementation | None"] = relationship()
    evidence: Mapped["EvidenceRecord | None"] = relationship()

    __table_args__ = (
        Index("ix_evidence_requests_organisation_id", "organisation_id"),
        Index("ix_evidence_requests_assignee_id", "assignee_id"),
        Index("ix_evidence_requests_status", "status"),
        Index("ix_evidence_requests_due_date", "due_date"),
    )
