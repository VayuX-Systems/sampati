# SPDX-License-Identifier: Apache-2.0
"""Base model with common fields and RLS support."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, String, Uuid, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Base class for all models with common fields."""
    pass


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class OrganisationMixin:
    """Mixin for organisation_id with RLS support."""
    
    @declared_attr.directive
    def organisation_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(
            Uuid,
            nullable=False,
            index=True,
            comment="Tenant organisation ID for row-level security",
        )


def generate_uuid7() -> uuid.UUID:
    """Generate a UUIDv7-like time-ordered UUID."""
    # Using uuid4 as fallback; in production use uuid-extensions or similar
    return uuid.uuid4()
