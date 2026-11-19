# SPDX-License-Identifier: Apache-2.0
"""User, Membership, and Role models."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, OrganisationMixin, TimestampMixin, generate_uuid7

if TYPE_CHECKING:
    from .organisation import Organisation


class BuiltInRole(enum.Enum):
    """Built-in roles per SAMPATI-GRANTH.md section 19.3."""
    ADMIN = "admin"
    COMPLIANCE_MANAGER = "compliance_manager"
    CONTROL_OWNER = "control_owner"
    CONTRIBUTOR = "contributor"
    EXECUTIVE = "executive"
    AUDITOR = "auditor"


class User(Base, TimestampMixin):
    """User identity (global, not tenant-scoped)."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    memberships: Mapped[list["Membership"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
    )


class Membership(Base, TimestampMixin, OrganisationMixin):
    """User membership in an organisation with a role."""

    __tablename__ = "memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(64), nullable=False)  # BuiltInRole or custom role ID

    # Relationships
    user: Mapped["User"] = relationship(back_populates="memberships")
    organisation: Mapped["Organisation"] = relationship(back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("user_id", "organisation_id", name="uq_membership_user_org"),
        Index("ix_memberships_user_id", "user_id"),
        Index("ix_memberships_organisation_id", "organisation_id"),
    )


class Role(Base, TimestampMixin, OrganisationMixin):
    """Custom role definition."""

    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    permissions: Mapped[list[str]] = mapped_column(default=list, nullable=False)
    is_system: Mapped[bool] = mapped_column(default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("organisation_id", "name", name="uq_role_org_name"),
    )
