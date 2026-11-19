# SPDX-License-Identifier: Apache-2.0
"""Audit logging service."""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator
from uuid import uuid4

from sampati_core_domain.models import AuditLog
from sampati_api.database import get_session_factory


class AuditService:
    """Service for writing audit log entries."""

    def __init__(self) -> None:
        self._session_factory = get_session_factory()

    @asynccontextmanager
    async def _session(self) -> AsyncGenerator[Any, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def log(
        self,
        organisation_id: str,
        actor_id: str | None,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
        request_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Write an audit log entry."""
        entry = AuditLog(
            id=uuid4(),
            organisation_id=organisation_id,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            before=before,
            after=after,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(timezone.utc),
        )
        
        async with self._session() as session:
            session.add(entry)
            await session.flush()
            return entry

    async def log_create(
        self,
        organisation_id: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        after: dict[str, Any],
        request_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Log a create action."""
        return await self.log(
            organisation_id=organisation_id,
            actor_id=actor_id,
            action="create",
            resource_type=resource_type,
            resource_id=resource_id,
            before=None,
            after=after,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def log_update(
        self,
        organisation_id: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        before: dict[str, Any],
        after: dict[str, Any],
        request_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Log an update action."""
        return await self.log(
            organisation_id=organisation_id,
            actor_id=actor_id,
            action="update",
            resource_type=resource_type,
            resource_id=resource_id,
            before=before,
            after=after,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def log_delete(
        self,
        organisation_id: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        before: dict[str, Any],
        request_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Log a delete action."""
        return await self.log(
            organisation_id=organisation_id,
            actor_id=actor_id,
            action="delete",
            resource_type=resource_type,
            resource_id=resource_id,
            before=before,
            after=None,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
