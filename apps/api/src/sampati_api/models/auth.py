# SPDX-License-Identifier: Apache-2.0
"""Authentication models: Session and API Token."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, OrganisationMixin, TimestampMixin, generate_uuid7

if TYPE_CHECKING:
    from .user import User


class SessionStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class Session(Base, TimestampMixin, OrganisationMixin):
    """User session with MFA state."""

    __tablename__ = "sessions"

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
    session_token_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    mfa_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    mfa_method: Mapped[str | None] = mapped_column(String(32), nullable=True)  # totp, webauthn
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        default=SessionStatus.ACTIVE,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_organisation_id", "organisation_id"),
        Index("ix_sessions_token_hash", "session_token_hash"),
        Index("ix_sessions_expires_at", "expires_at"),
    )

    @classmethod
    def create(cls, user_id: uuid.UUID, organisation_id: uuid.UUID, ttl_minutes: int = 30) -> "Session":
        """Create a new session with expiry."""
        return cls(
            user_id=user_id,
            organisation_id=organisation_id,
            session_token_hash="",  # Set by caller after hashing
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes),
        )


class APITokenScope(enum.Enum):
    """API token scopes."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    AUDIT = "audit"
    EVIDENCE_READ = "evidence:read"
    EVIDENCE_WRITE = "evidence:write"
    CONTROL_READ = "control:read"
    CONTROL_WRITE = "control:write"
    FRAMEWORK_READ = "framework:read"
    PLUGIN_READ = "plugin:read"
    PLUGIN_WRITE = "plugin:write"


class APIToken(Base, TimestampMixin, OrganisationMixin):
    """Scoped API token for programmatic access."""

    __tablename__ = "api_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid7,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    scopes: Mapped[list[str]] = mapped_column(default=list, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_api_tokens_organisation_id", "organisation_id"),
        Index("ix_api_tokens_token_hash", "token_hash"),
    )

    @classmethod
    def create(
        cls,
        organisation_id: uuid.UUID,
        name: str,
        scopes: list[str],
        ttl_days: int | None = None,
    ) -> "APIToken":
        """Create a new API token."""
        expires_at = None
        if ttl_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=ttl_days)
        return cls(
            organisation_id=organisation_id,
            name=name,
            token_hash="",  # Set by caller after hashing
            scopes=scopes,
            expires_at=expires_at,
        )

    def is_valid(self) -> bool:
        """Check if token is valid (not revoked, not expired)."""
        if self.revoked_at:
            return False
        if self.expires_at and self.expires_at < datetime.now(timezone.utc):
            return False
        return True
