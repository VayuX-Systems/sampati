# SPDX-License-Identifier: Apache-2.0
"""OIDC provider integration for Google and Microsoft."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from ..config import get_settings


@dataclass
class OIDCUserInfo:
    """User information from OIDC provider."""
    sub: str
    email: str
    name: str
    picture: str | None = None
    email_verified: bool = False


class OIDCProvider:
    """OIDC provider for Google and Microsoft."""

    PROVIDERS = {
        "google": {
            "issuer": "https://accounts.google.com",
            "auth_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://www.googleapis.com/oauth2/v3/userinfo",
            "scopes": ["openid", "email", "profile"],
        },
        "microsoft": {
            "issuer": "https://login.microsoftonline.com/{tenant}/v2.0",
            "auth_endpoint": "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
            "token_endpoint": "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
            "userinfo_endpoint": "https://graph.microsoft.com/oidc/userinfo",
            "scopes": ["openid", "email", "profile", "User.Read"],
        },
    }

    def __init__(self, provider_name: str, client_id: str, client_secret: str, redirect_uri: str, tenant: str | None = None) -> None:
        if provider_name not in self.PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        self.provider_name = provider_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.tenant = tenant
        self.config = self.PROVIDERS[provider_name].copy()
        
        # Format Microsoft endpoints with tenant
        if provider_name == "microsoft" and tenant:
            for key in ["issuer", "auth_endpoint", "token_endpoint", "userinfo_endpoint"]:
                self.config[key] = self.config[key].format(tenant=tenant)

    def get_authorization_url(self, state: str, nonce: str | None = None) -> str:
        """Generate the authorization URL for the OIDC flow."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.config["scopes"]),
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        if nonce:
            params["nonce"] = nonce
        
        return f"{self.config['auth_endpoint']}?{urlencode(params)}"

    async def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        """Exchange authorization code for access/refresh tokens."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config["token_endpoint"],
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code",
                },
                headers={"Accept": "application/json"},
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> OIDCUserInfo:
        """Get user info from the provider."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.config["userinfo_endpoint"],
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            
            # Normalize provider-specific fields
            if self.provider_name == "google":
                return OIDCUserInfo(
                    sub=data["sub"],
                    email=data["email"],
                    name=data.get("name", ""),
                    picture=data.get("picture"),
                    email_verified=data.get("email_verified", False),
                )
            elif self.provider_name == "microsoft":
                return OIDCUserInfo(
                    sub=data["sub"],
                    email=data.get("preferred_username", data.get("email", "")),
                    name=data.get("name", ""),
                    email_verified=True,  # Microsoft emails are verified
                )
            
            raise ValueError(f"Unknown provider: {self.provider_name}")


def get_oidc_provider(provider_name: str) -> OIDCProvider | None:
    """Get configured OIDC provider from settings."""
    settings = get_settings()
    
    if provider_name == "google" and settings.oidc_client_id and settings.oidc_client_secret:
        # For Google, we use the same client_id/secret for both
        return OIDCProvider(
            provider_name="google",
            client_id=settings.oidc_client_id,
            client_secret=settings.oidc_client_secret,
            redirect_uri=f"{settings.base_url}/api/v1/auth/oidc/google/callback",
        )
    elif provider_name == "microsoft" and settings.oidc_client_id and settings.oidc_client_secret:
        # Microsoft needs tenant
        tenant = settings.oidc_issuer.split("/")[-2] if settings.oidc_issuer else "common"
        return OIDCProvider(
            provider_name="microsoft",
            client_id=settings.oidc_client_id,
            client_secret=settings.oidc_client_secret,
            redirect_uri=f"{settings.base_url}/api/v1/auth/oidc/microsoft/callback",
            tenant=tenant,
        )
    
    return None
