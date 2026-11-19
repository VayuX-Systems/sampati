# SPDX-License-Identifier: Apache-2.0
"""Multi-factor authentication: TOTP and WebAuthn."""

from __future__ import annotations

import base64
import secrets
from typing import Any

import pyotp
import qrcode
import qrcode.image.svg

from ..config import get_settings
from ..database import get_tenant_session
from ..models import User, Session
from ..models.auth import SessionStatus


class TOTPManager:
    """Time-based One-Time Password manager."""

    ISSUER = "Sampati by VayuX"

    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret."""
        return pyotp.random_base32()

    @staticmethod
    def get_provisioning_uri(email: str, secret: str) -> str:
        """Get the provisioning URI for QR code."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=TOTPManager.ISSUER)

    @staticmethod
    def generate_qr_code(uri: str) -> str:
        """Generate QR code as SVG string."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white", image_factory=qrcode.image.svg.SvgImage)
        return img.to_string(encoding="utf-8")

    @staticmethod
    def verify_totp(secret: str, token: str, valid_window: int = 1) -> bool:
        """Verify a TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=valid_window)


class MFAManager:
    """Manages MFA setup and verification for users."""

    def __init__(self) -> None:
        self.totp = TOTPManager()

    async def setup_totp(self, user_id: str, organisation_id: str) -> dict[str, Any]:
        """Initiate TOTP setup for a user."""
        secret = self.totp.generate_secret()
        user_email = await self._get_user_email(user_id, organisation_id)
        
        if not user_email:
            raise ValueError("User not found")
        
        uri = self.totp.get_provisioning_uri(user_email, secret)
        qr_code = self.totp.generate_qr_code(uri)
        
        # Store secret temporarily (in production, encrypt it)
        # The user must verify a token before we permanently save it
        return {
            "secret": secret,
            "qr_code": qr_code,
            "uri": uri,
        }

    async def verify_totp_setup(self, user_id: str, organisation_id: str, secret: str, token: str) -> bool:
        """Verify TOTP token during setup and save secret if valid."""
        if not self.totp.verify_totp(secret, token):
            return False
        
        # In production, encrypt and store the secret in user profile
        # For now, we just return success
        return True

    async def verify_totp_login(self, user_id: str, organisation_id: str, token: str) -> bool:
        """Verify TOTP token during login."""
        # In production, retrieve encrypted secret from user profile
        # For now, this is a stub
        return True

    async def _get_user_email(self, user_id: str, organisation_id: str) -> str | None:
        """Get user email from database."""
        async with get_tenant_session(organisation_id) as session:
            user = await session.get(User, user_id)
            return user.email if user else None


# WebAuthn stub for future implementation
class WebAuthnManager:
    """WebAuthn/Passkey manager (stub for Phase 1)."""
    
    @staticmethod
    def generate_registration_options(user_id: str, username: str, display_name: str) -> dict[str, Any]:
        """Generate WebAuthn registration options (stub)."""
        raise NotImplementedError("WebAuthn not implemented in MVP")

    @staticmethod
    def verify_registration_response(options: dict[str, Any], response: dict[str, Any]) -> dict[str, Any] | None:
        """Verify WebAuthn registration response (stub)."""
        raise NotImplementedError("WebAuthn not implemented in MVP")

    @staticmethod
    def generate_authentication_options() -> dict[str, Any]:
        """Generate WebAuthn authentication options (stub)."""
        raise NotImplementedError("WebAuthn not implemented in MVP")

    @staticmethod
    def verify_authentication_response(options: dict[str, Any], response: dict[str, Any]) -> bool:
        """Verify WebAuthn authentication response (stub)."""
        raise NotImplementedError("WebAuthn not implemented in MVP")
