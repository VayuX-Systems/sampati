# SPDX-License-Identifier: Apache-2.0
"""Session management routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ....auth.dependencies import get_current_user
from ....database import get_tenant_session
from ....models import Session, SessionStatus

router = APIRouter(prefix="/sessions", tags=["auth"])


class SessionResponse(BaseModel):
    id: str
    mfa_verified: bool
    mfa_method: str | None
    status: str
    expires_at: str
    created_at: str


@router.get("", response_model=list[SessionResponse])
async def list_sessions(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[SessionResponse]:
    """List active sessions for current user."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Session)
            .where(Session.user_id == current_user.user_id)
            .where(Session.status == SessionStatus.ACTIVE)
            .order_by(Session.created_at.desc())
        )
        sessions = result.scalars().all()
        
        return [
            SessionResponse(
                id=str(s.id),
                mfa_verified=s.mfa_verified,
                mfa_method=s.mfa_method,
                status=s.status.value,
                expires_at=s.expires_at.isoformat(),
                created_at=s.created_at.isoformat(),
            )
            for s in sessions
        ]


@router.delete("/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, str]:
    """Revoke a session."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Session).where(Session.id == session_id)
        )
        session_obj = result.scalar_one_or_none()
        
        if not session_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )
        
        if session_obj.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot revoke another user's session",
            )
        
        session_obj.status = SessionStatus.REVOKED
        await session.commit()
        
        return {"message": "Session revoked"}


@router.delete("")
async def revoke_all_sessions(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, str]:
    """Revoke all sessions for current user (except current)."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select, update
        await session.execute(
            update(Session)
            .where(Session.user_id == current_user.user_id)
            .where(Session.id != current_user.session_id)
            .values(status=SessionStatus.REVOKED)
        )
        await session.commit()
        
        return {"message": "All other sessions revoked"}
