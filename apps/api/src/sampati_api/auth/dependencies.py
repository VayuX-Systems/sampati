# SPDX-License-Identifier: Apache-2.0
"""FastAPI authentication dependencies."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, Request, status
from pydantic import BaseModel

from .jwt_handler import JWTHandler, create_jwt_handler


class CurrentUser(BaseModel):
    """Current authenticated user."""
    user_id: str
    organisation_id: str
    roles: list[str] = []
    scopes: list[str] = []
    mfa_verified: bool = False
    session_id: str | None = None


async def get_current_user(
    request: Request,
    authorization: Annotated[Optional[str], Header()] = None,
    jwt_handler: Annotated[JWTHandler, Depends(create_jwt_handler)] = None,
) -> CurrentUser:
    """Extract and validate current user from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization[7:]  # Remove "Bearer "
    
    try:
        payload = jwt_handler.decode_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return CurrentUser(
        user_id=payload.sub,
        organisation_id=payload.org,
        roles=payload.roles,
        scopes=payload.scopes,
        mfa_verified=payload.mfa_verified,
        session_id=payload.session_id,
    )


async def get_current_organisation(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> str:
    """Get current organisation ID."""
    return current_user.organisation_id


def require_role(*allowed_roles: str):
    """Dependency that requires one of the specified roles."""
    async def role_checker(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        # Admin always has access
        if "admin" in current_user.roles:
            return current_user
        
        # Check if user has any of the required roles
        if not any(role in current_user.roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role(s): {', '.join(allowed_roles)}",
            )
        
        return current_user
    
    return role_checker


def require_scope(*allowed_scopes: str):
    """Dependency that requires one of the specified scopes."""
    async def scope_checker(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        # Admin scope covers everything
        if "admin" in current_user.scopes:
            return current_user
        
        # Check if user has any of the required scopes
        if not any(scope in current_user.scopes for scope in allowed_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required scope(s): {', '.join(allowed_scopes)}",
            )
        
        return current_user
    
    return scope_checker


def require_mfa():
    """Dependency that requires MFA verification."""
    async def mfa_checker(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if not current_user.mfa_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Multi-factor authentication required",
            )
        return current_user
    
    return mfa_checker
