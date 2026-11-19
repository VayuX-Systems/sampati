# SPDX-License-Identifier: Apache-2.0
"""Extension points for the Enterprise Edition to implement.

These interfaces are defined in the Community Edition and implemented
by the Enterprise Edition. The Community Edition provides no-op
implementations by default.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SAMLConfig:
    entity_id: str
    sso_url: str
    x509_cert: str
    attribute_mapping: dict[str, str]


@dataclass
class SCIMConfig:
    base_url: str
    bearer_token: str
    filter: str = ""


class SSOProvider(ABC):
    """Interface for SSO providers (SAML, OIDC)."""

    @abstractmethod
    def authenticate(self, request: Any) -> Optional[str]:
        """Authenticate a request and return user ID if successful."""
        ...

    @abstractmethod
    def get_login_url(self, redirect_url: str) -> str:
        """Get the SSO login URL."""
        ...


class SAMLProvider(SSOProvider):
    """SAML 2.0 provider interface."""

    @abstractmethod
    def configure(self, config: SAMLConfig) -> None:
        ...

    @abstractmethod
    def parse_assertion(self, saml_response: str) -> dict[str, Any]:
        """Parse SAML assertion and return user attributes."""
        ...


class SCIMProvider(ABC):
    """SCIM 2.0 user provisioning interface."""

    @abstractmethod
    def configure(self, config: SCIMConfig) -> None:
        ...

    @abstractmethod
    def list_users(self, filter: str = "") -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        ...

    @abstractmethod
    def create_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        ...


class AuditExportProvider(ABC):
    """Advanced audit export interface (enterprise)."""

    @abstractmethod
    def export_legal_hold(self, audit_project_id: str) -> bytes:
        """Export audit pack with legal hold metadata."""
        ...

    @abstractmethod
    def export_dual_approval(self, audit_project_id: str, approvers: list[str]) -> bytes:
        """Export audit pack requiring dual approval."""
        ...

    @abstractmethod
    def export_certified(self, audit_project_id: str) -> bytes:
        """Export certified audit pack with tamper-proof seal."""
        ...


class LicenceProvider(ABC):
    """License validation for enterprise features."""

    @abstractmethod
    def validate(self, licence_key: str) -> tuple[bool, dict[str, Any]]:
        """Validate a license key. Returns (is_valid, licence_info)."""
        ...

    @abstractmethod
    def get_limits(self, licence_key: str) -> dict[str, int]:
        """Get plan limits for a license key."""
        ...


class RegulatoryFeedProvider(ABC):
    """Live regulatory update feed (enterprise)."""

    @abstractmethod
    def fetch_updates(self, since: str) -> list[dict[str, Any]]:
        """Fetch pack updates since a date."""
        ...

    @abstractmethod
    def get_pack_diff(self, pack_id: str, from_version: str, to_version: str) -> dict[str, Any]:
        """Get diff between pack versions."""
        ...


class HAProvider(ABC):
    """High availability / multi-region support."""

    @abstractmethod
    def get_replica_status(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def promote_replica(self, region: str) -> bool:
        ...


class WhiteLabelProvider(ABC):
    """White-label customization."""

    @abstractmethod
    def get_branding(self, organisation_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    def apply_branding(self, organisation_id: str, branding: dict[str, Any]) -> None:
        ...


class PartnerConsoleProvider(ABC):
    """Multi-client console for partners."""

    @abstractmethod
    def list_clients(self, partner_id: str) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def switch_client(self, partner_id: str, client_org_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_rollup(self, partner_id: str) -> dict[str, Any]:
        ...


# Default no-op implementations for Community Edition
class NoOpSAMLProvider(SAMLProvider):
    def configure(self, config: SAMLConfig) -> None:
        raise NotImplementedError("SAML not available in Community Edition")

    def authenticate(self, request: Any) -> Optional[str]:
        return None

    def get_login_url(self, redirect_url: str) -> str:
        raise NotImplementedError("SAML not available in Community Edition")

    def parse_assertion(self, saml_response: str) -> dict[str, Any]:
        raise NotImplementedError("SAML not available in Community Edition")


class NoOpSCIMProvider(SCIMProvider):
    def configure(self, config: SCIMConfig) -> None:
        raise NotImplementedError("SCIM not available in Community Edition")

    def list_users(self, filter: str = "") -> list[dict[str, Any]]:
        raise NotImplementedError("SCIM not available in Community Edition")

    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        raise NotImplementedError("SCIM not available in Community Edition")

    def create_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("SCIM not available in Community Edition")

    def update_user(self, user_id: str, user_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("SCIM not available in Community Edition")

    def delete_user(self, user_id: str) -> None:
        raise NotImplementedError("SCIM not available in Community Edition")


class NoOpAuditExportProvider(AuditExportProvider):
    def export_legal_hold(self, audit_project_id: str) -> bytes:
        raise NotImplementedError("Advanced audit export not available in Community Edition")

    def export_dual_approval(self, audit_project_id: str, approvers: list[str]) -> bytes:
        raise NotImplementedError("Advanced audit export not available in Community Edition")

    def export_certified(self, audit_project_id: str) -> bytes:
        raise NotImplementedError("Advanced audit export not available in Community Edition")


class NoOpLicenceProvider(LicenceProvider):
    def validate(self, licence_key: str) -> tuple[bool, dict[str, Any]]:
        return False, {}

    def get_limits(self, licence_key: str) -> dict[str, int]:
        return {}


class NoOpRegulatoryFeedProvider(RegulatoryFeedProvider):
    def fetch_updates(self, since: str) -> list[dict[str, Any]]:
        return []

    def get_pack_diff(self, pack_id: str, from_version: str, to_version: str) -> dict[str, Any]:
        return {}


class NoOpHAProvider(HAProvider):
    def get_replica_status(self) -> dict[str, Any]:
        return {"mode": "standalone"}

    def promote_replica(self, region: str) -> bool:
        return False


class NoOpWhiteLabelProvider(WhiteLabelProvider):
    def get_branding(self, organisation_id: str) -> dict[str, Any]:
        return {}

    def apply_branding(self, organisation_id: str, branding: dict[str, Any]) -> None:
        pass


class NoOpPartnerConsoleProvider(PartnerConsoleProvider):
    def list_clients(self, partner_id: str) -> list[dict[str, Any]]:
        return []

    def switch_client(self, partner_id: str, client_org_id: str) -> dict[str, Any]:
        return {}

    def get_rollup(self, partner_id: str) -> dict[str, Any]:
        return {}


# Registry for runtime injection by Enterprise Edition
_saml_provider: SAMLProvider = NoOpSAMLProvider()
_scim_provider: SCIMProvider = NoOpSCIMProvider()
_audit_export_provider: AuditExportProvider = NoOpAuditExportProvider()
_licence_provider: LicenceProvider = NoOpLicenceProvider()
_regulatory_feed_provider: RegulatoryFeedProvider = NoOpRegulatoryFeedProvider()
_ha_provider: HAProvider = NoOpHAProvider()
_white_label_provider: WhiteLabelProvider = NoOpWhiteLabelProvider()
_partner_console_provider: PartnerConsoleProvider = NoOpPartnerConsoleProvider()


def set_saml_provider(provider: SAMLProvider) -> None:
    global _saml_provider
    _saml_provider = provider


def get_saml_provider() -> SAMLProvider:
    return _saml_provider


def set_scim_provider(provider: SCIMProvider) -> None:
    global _scim_provider
    _scim_provider = provider


def get_scim_provider() -> SCIMProvider:
    return _scim_provider


def set_audit_export_provider(provider: AuditExportProvider) -> None:
    global _audit_export_provider
    _audit_export_provider = provider


def get_audit_export_provider() -> AuditExportProvider:
    return _audit_export_provider


def set_licence_provider(provider: LicenceProvider) -> None:
    global _licence_provider
    _licence_provider = provider


def get_licence_provider() -> LicenceProvider:
    return _licence_provider


def set_regulatory_feed_provider(provider: RegulatoryFeedProvider) -> None:
    global _regulatory_feed_provider
    _regulatory_feed_provider = provider


def get_regulatory_feed_provider() -> RegulatoryFeedProvider:
    return _regulatory_feed_provider


def set_ha_provider(provider: HAProvider) -> None:
    global _ha_provider
    _ha_provider = provider


def get_ha_provider() -> HAProvider:
    return _ha_provider


def set_white_label_provider(provider: WhiteLabelProvider) -> None:
    global _white_label_provider
    _white_label_provider = provider


def get_white_label_provider() -> WhiteLabelProvider:
    return _white_label_provider


def set_partner_console_provider(provider: PartnerConsoleProvider) -> None:
    global _partner_console_provider
    _partner_console_provider = provider


def get_partner_console_provider() -> PartnerConsoleProvider:
    return _partner_console_provider
