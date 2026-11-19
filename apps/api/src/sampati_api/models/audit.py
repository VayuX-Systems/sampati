# SPDX-License-Identifier: Apache-2.0
"""Audit log model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, OrganisationMixin, TimestampMixin, generate_uuid7

if TYPE_CHECKING:
    from .user import User
    from .organisation import Organisation


class AuditLog(Base, OrganisationMixin):
    """Append-only audit log for all write operations."""

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False)  # create, update, delete, login, etc.
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)  # organisation, entity, control, evidence, etc.
    resource_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    before: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    request_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    # No updated_at for audit logs - they are append-only
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index("ix_audit_logs_organisation_id_created_at", "organisation_id", "created_at"),
        Index("ix_audit_logs_actor_id", "actor_id"),
        Index("ix_audit_logs_resource", "resource_type", "resource_id"),
        Index("ix_audit_logs_request_id", "request_id"),
    )
