# SPDX-License-Identifier: Apache-2.0
"""Sampati Extension Points - Enterprise Edition interfaces."""

from .extension_points import (
    SSOProvider, SAMLProvider, SCIMProvider,
    AuditExportProvider, LicenceProvider,
    RegulatoryFeedProvider, HAProvider,
    WhiteLabelProvider, PartnerConsoleProvider,
    NoOpSAMLProvider, NoOpSCIMProvider, NoOpAuditExportProvider,
    NoOpLicenceProvider, NoOpRegulatoryFeedProvider, NoOpHAProvider,
    NoOpWhiteLabelProvider, NoOpPartnerConsoleProvider,
    set_saml_provider, get_saml_provider,
    set_scim_provider, get_scim_provider,
    set_audit_export_provider, get_audit_export_provider,
    set_licence_provider, get_licence_provider,
    set_regulatory_feed_provider, get_regulatory_feed_provider,
    set_ha_provider, get_ha_provider,
    set_white_label_provider, get_white_label_provider,
    set_partner_console_provider, get_partner_console_provider,
)

__all__ = [
    "SSOProvider", "SAMLProvider", "SCIMProvider",
    "AuditExportProvider", "LicenceProvider",
    "RegulatoryFeedProvider", "HAProvider",
    "WhiteLabelProvider", "PartnerConsoleProvider",
    "NoOpSAMLProvider", "NoOpSCIMProvider", "NoOpAuditExportProvider",
    "NoOpLicenceProvider", "NoOpRegulatoryFeedProvider", "NoOpHAProvider",
    "NoOpWhiteLabelProvider", "NoOpPartnerConsoleProvider",
    "set_saml_provider", "get_saml_provider",
    "set_scim_provider", "get_scim_provider",
    "set_audit_export_provider", "get_audit_export_provider",
    "set_licence_provider", "get_licence_provider",
    "set_regulatory_feed_provider", "get_regulatory_feed_provider",
    "set_ha_provider", "get_ha_provider",
    "set_white_label_provider", "get_white_label_provider",
    "set_partner_console_provider", "get_partner_console_provider",
]
