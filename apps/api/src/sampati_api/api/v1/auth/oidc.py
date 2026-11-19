# SPDX-License-Identifier: Apache-2.0
"""OIDC authentication routes."""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ....auth import OIDCProvider, get_oidc_provider
from ....auth.dependencies import get_current_user
from ....auth.jwt_handler import create_jwt_handler
from ....config import get_settings
from ....database import get_tenant_session
from ....models import User, Membership, Session
from ....models.auth import SessionStatus

router = APIRouter(prefix="/oidc", tags=["auth"])


class OIDCLoginRequest(BaseModel):
    provider: str  # google, microsoft
    redirect_url: str | None = None


class OIDCCallbackRequest(BaseModel):
    code: str
    state: str
    provider: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# In-memory state store (use Redis in production)
_oidc_states: dict[str, dict] = {}


@router.get("/providers")
async def list_providers() -> dict[str, list[str]]:
    """List available OIDC providers."""
    settings = get_settings()
    providers = []
    if settings.oidc_client_id and settings.oidc_client_secret:
        providers.append("google")
        providers.append("microsoft")
    return {"providers": providers}


@router.post("/login")
async def oidc_login(
    request: OIDCLoginRequest,
    response: Response,
) -> dict[str, str]:
    """Initiate OIDC login flow."""
    provider = get_oidc_provider(request.provider)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider {request.provider} not configured",
        )
    
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    
    # Store state for callback verification
    _oidc_states[state] = {
        "provider": request.provider,
        "nonce": nonce,
        "redirect_url": request.redirect_url or "/",
    }
    
    auth_url = provider.get_authorization_url(state=state, nonce=nonce)
    
    return {"authorization_url": auth_url, "state": state}


@router.get("/{provider}/callback")
async def oidc_callback(
    provider: str,
    code: str = Query(...),
    state: str = Query(...),
    error: str | None = Query(None),
    error_description: str | None = Query(None),
) -> RedirectResponse:
    """Handle OIDC callback."""
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OIDC error: {error} - {error_description}",
        )
    
    # Verify state
    stored = _oidc_states.pop(state, None)
    if not stored or stored["provider"] != provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state",
        )
    
    oidc_provider = get_oidc_provider(provider)
    if not oidc_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider {provider} not configured",
        )
    
    # Exchange code for tokens
    tokens = await oidc_provider.exchange_code_for_tokens(code)
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token received",
        )
    
    # Get user info
    user_info = await oidc_provider.get_user_info(access_token)
    
    # Find or create user
    settings = get_settings()
    # For MVP, we'll use a default organisation or create one
    # In production, this would be more complex
    org_id = "00000000-0000-0000-0000-000000000001"  # Default org
    
    async with get_tenant_session(org_id) as session:
        # Find user by email
        from sqlalchemy import select
        result = await session.execute(
            select(User).where(User.email == user_info.email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                email=user_info.email,
                name=user_info.name,
                avatar_url=user_info.picture,
            )
            session.add(user)
            await session.flush()
            
            # Create membership with default role
            membership = Membership(
                user_id=user.id,
                organisation_id=org_id,
                role="contributor",
            )
            session.add(membership)
        
        # Create session
        session_obj = Session.create(
            user_id=user.id,
            organisation_id=org_id,
            ttl_minutes=settings.access_token_expire_minutes,
        )
        session.add(session_obj)
        await session.flush()
        
        # Create JWT
        jwt_handler = create_jwt_handler()
        jwt_token = jwt_handler.create_access_token(
            user_id=str(user.id),
            organisation_id=str(org_id),
            roles=["contributor"],
            mfa_verified=False,
            session_id=str(session_obj.id),
        )
        
        # Set session cookie
        response = RedirectResponse(url=stored["redirect_url"])
        response.set_cookie(
            key="session",
            value=jwt_token,
            httponly=True,
            secure=settings.env == "prod",
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60,
        )
        
        return response


@router.post("/logout")
async def oidc_logout(
    current_user: Annotated[dict, Depends(get_current_user)],
    response: Response,
) -> dict[str, str]:
    """Log out current user."""
    response.delete_cookie(key="session")
    return {"message": "Logged out successfully"}
