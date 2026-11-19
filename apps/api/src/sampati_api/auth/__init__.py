# SPDX-License-Identifier: Apache-2.0
"""Authentication module for Sampati API."""

from .jwt_handler import JWTHandler, create_jwt_handler
from .oidc import OIDCProvider, get_oidc_provider
from .mfa import MFAManager, TOTPManager
from .dependencies import get_current_user, get_current_organisation, require_role

__all__ = [
    "JWTHandler",
    "create_jwt_handler",
    "OIDCProvider",
    "get_oidc_provider",
    "MFAManager",
    "TOTPManager",
    "get_current_user",
    "get_current_organisation",
    "require_role",
]
