# SPDX-License-Identifier: Apache-2.0
"""JWT token handling for authentication."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

from jose import jwt
from pydantic import BaseModel

from ..config import get_settings


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: str  # user_id
    org: str  # organisation_id
    roles: list[str] = []
    scopes: list[str] = []
    mfa_verified: bool = False
    session_id: str | None = None
    exp: int
    iat: int
    jti: str


class JWTHandler:
    """Handles JWT creation and validation."""

    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
        self,
        user_id: str,
        organisation_id: str,
        roles: list[str] | None = None,
        scopes: list[str] | None = None,
        mfa_verified: bool = False,
        session_id: str | None = None,
    ) -> str:
        """Create a new access token."""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)

        payload = TokenPayload(
            sub=user_id,
            org=organisation_id,
            roles=roles or [],
            scopes=scopes or [],
            mfa_verified=mfa_verified,
            session_id=session_id,
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
            jti=secrets.token_urlsafe(16),
        )

        return jwt.encode(payload.model_dump(), self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        """Decode and validate a token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError as e:
            raise ValueError(f"Invalid token: {e}")

    def create_refresh_token(self, user_id: str, organisation_id: str, expires_days: int = 7) -> str:
        """Create a long-lived refresh token."""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=expires_days)

        payload = {
            "sub": user_id,
            "org": organisation_id,
            "type": "refresh",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": secrets.token_urlsafe(16),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


def create_jwt_handler() -> JWTHandler:
    """Create JWT handler from settings."""
    settings = get_settings()
    return JWTHandler(
        secret_key=settings.secret_key,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
