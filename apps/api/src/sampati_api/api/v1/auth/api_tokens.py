# SPDX-License-Identifier: Apache-2.0
"""API token management routes."""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ....auth.dependencies import get_current_user, require_role
from ....database import get_tenant_session
from ....models import APIToken

router = APIRouter(prefix="/api-tokens", tags=["auth"])


class APITokenCreate(BaseModel):
    name: str
    scopes: list[str]
    expires_in_days: int | None = None


class APITokenResponse(BaseModel):
    id: str
    name: str
    scopes: list[str]
    expires_at: str | None
    last_used_at: str | None
    created_at: str
    token: str | None = None  # Only returned on creation


class APITokenListResponse(BaseModel):
    id: str
    name: str
    scopes: list[str]
    expires_at: str | None
    last_used_at: str | None
    created_at: str
    revoked_at: str | None


@router.post("", response_model=APITokenResponse, status_code=status.HTTP_201_CREATED)
async def create_api_token(
    request: APITokenCreate,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> APITokenResponse:
    """Create a new API token."""
    # Generate token
    raw_token = f"spt_{secrets.token_urlsafe(32)}"
    token_hash = secrets.token_urlsafe(32)  # In production, hash properly
    
    async with get_tenant_session(current_user.organisation_id) as session:
        api_token = APIToken.create(
            organisation_id=current_user.organisation_id,
            name=request.name,
            scopes=request.scopes,
            ttl_days=request.expires_in_days,
        )
        api_token.token_hash = token_hash
        session.add(api_token)
        await session.flush()
        
        return APITokenResponse(
            id=str(api_token.id),
            name=api_token.name,
            scopes=api_token.scopes,
            expires_at=api_token.expires_at.isoformat() if api_token.expires_at else None,
            last_used_at=None,
            created_at=api_token.created_at.isoformat(),
            token=raw_token,  # Only returned once
        )


@router.get("", response_model=list[APITokenListResponse])
async def list_api_tokens(
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> list[APITokenListResponse]:
    """List API tokens for organisation."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        result = await session.execute(
            select(APIToken)
            .where(APIToken.organisation_id == current_user.organisation_id)
            .order_by(APIToken.created_at.desc())
        )
        tokens = result.scalars().all()
        
        return [
            APITokenListResponse(
                id=str(t.id),
                name=t.name,
                scopes=t.scopes,
                expires_at=t.expires_at.isoformat() if t.expires_at else None,
                last_used_at=t.last_used_at.isoformat() if t.last_used_at else None,
                created_at=t.created_at.isoformat(),
                revoked_at=t.revoked_at.isoformat() if t.revoked_at else None,
            )
            for t in tokens
        ]


@router.delete("/{token_id}")
async def revoke_api_token(
    token_id: str,
    current_user: Annotated[dict, Depends(require_role("admin", "compliance_manager"))],
) -> dict[str, str]:
    """Revoke an API token."""
    async with get_tenant_session(current_user.organisation_id) as session:
        from sqlalchemy import select
        from datetime import datetime, timezone
        
        result = await session.execute(
            select(APIToken).where(APIToken.id == token_id)
        )
        api_token = result.scalar_one_or_none()
        
        if not api_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API token not found",
            )
        
        if api_token.organisation_id != current_user.organisation_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot revoke token from another organisation",
            )
        
        api_token.revoked_at = datetime.now(timezone.utc)
        await session.commit()
        
        return {"message": "API token revoked"}
