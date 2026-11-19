# SPDX-License-Identifier: Apache-2.0
"""MFA authentication routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ....auth.dependencies import get_current_user, require_mfa
from ....auth.mfa import MFAManager, TOTPManager

router = APIRouter(prefix="/mfa", tags=["auth"])


class TOTPSetupRequest(BaseModel):
    pass


class TOTPSetupResponse(BaseModel):
    secret: str
    qr_code: str
    uri: str


class TOTPVerifyRequest(BaseModel):
    secret: str
    token: str


class TOTPVerifyResponse(BaseModel):
    verified: bool


class TOTPLoginRequest(BaseModel):
    token: str


@router.post("/totp/setup", response_model=TOTPSetupResponse)
async def setup_totp(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> TOTPSetupResponse:
    """Initiate TOTP setup."""
    mfa_manager = MFAManager()
    result = await mfa_manager.setup_totp(
        user_id=current_user.user_id,
        organisation_id=current_user.organisation_id,
    )
    return TOTPSetupResponse(**result)


@router.post("/totp/verify-setup", response_model=TOTPVerifyResponse)
async def verify_totp_setup(
    request: TOTPVerifyRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> TOTPVerifyResponse:
    """Verify TOTP setup and save secret."""
    mfa_manager = MFAManager()
    verified = await mfa_manager.verify_totp_setup(
        user_id=current_user.user_id,
        organisation_id=current_user.organisation_id,
        secret=request.secret,
        token=request.token,
    )
    return TOTPVerifyResponse(verified=verified)


@router.post("/totp/login", response_model=TOTPVerifyResponse)
async def verify_totp_login(
    request: TOTPLoginRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> TOTPVerifyResponse:
    """Verify TOTP during login (step-up auth)."""
    mfa_manager = MFAManager()
    verified = await mfa_manager.verify_totp_login(
        user_id=current_user.user_id,
        organisation_id=current_user.organisation_id,
        token=request.token,
    )
    return TOTPVerifyResponse(verified=verified)


@router.get("/status")
async def mfa_status(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, bool]:
    """Get MFA status for current user."""
    # In production, check if user has TOTP/WebAuthn configured
    return {
        "totp_enabled": False,  # TODO: check user profile
        "webauthn_enabled": False,
        "mfa_verified": current_user.mfa_verified,
    }
