# SPDX-License-Identifier: Apache-2.0
"""Organisation and Entity models."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, OrganisationMixin, TimestampMixin, generate_uuid7

if TYPE_CHECKING:
    from .user import User, Membership


class OrganisationStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class EntityType(enum.Enum):
    LEGAL_ENTITY = "legal_entity"
    BUSINESS_UNIT = "business_unit"


class Organisation(Base, TimestampMixin):
    """Top-level tenant organisation."""

    __tablename__ = "organisations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
        comment="Unique organisation identifier",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    region: Mapped[str] = mapped_column(String(2), default="IN", nullable=False)
    status: Mapped[OrganisationStatus] = mapped_column(
        Enum(OrganisationStatus),
        default=OrganisationStatus.ACTIVE,
        nullable=False,
    )
    settings: Mapped[dict] = mapped_column(default=dict, nullable=False)

    # Relationships
    entities: Mapped[list["Entity"]] = relationship(back_populates="organisation", cascade="all, delete-orphan")
    memberships: Mapped[list["Membership"]] = relationship(back_populates="organisation", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_organisations_slug", "slug", unique=True),
    )


class Entity(Base, TimestampMixin, OrganisationMixin):
    """Legal entity or business unit within an organisation."""

    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[EntityType] = mapped_column(
        Enum(EntityType),
        default=EntityType.LEGAL_ENTITY,
        nullable=False,
    )
    parent_entity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("entities.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    organisation: Mapped["Organisation"] = relationship(back_populates="entities")
    parent_entity: Mapped["Entity | None"] = relationship(remote_side="Entity.id", backref="child_entities")

    __table_args__ = (
        UniqueConstraint("organisation_id", "name", name="uq_entity_org_name"),
        Index("ix_entities_organisation_id", "organisation_id"),
    )
