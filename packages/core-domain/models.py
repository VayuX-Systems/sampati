# SPDX-License-Identifier: Apache-2.0
"""Core domain models for Sampati Community Edition."""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def uuid7() -> str:
    """Generate a UUIDv7-like string (time-ordered)."""
    # Simplified - in production use uuid-extensions or similar
    return str(uuid.uuid4())


class OrganisationStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class EntityType(enum.Enum):
    LEGAL_ENTITY = "legal_entity"
    BUSINESS_UNIT = "business_unit"


class FrameworkStatus(enum.Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    PUBLISHED = "published"


class ControlStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    NOT_APPLICABLE = "not_applicable"


class MappingStrength(enum.Enum):
    FULL = "full"
    PARTIAL = "partial"


class EvidenceResult(enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    INFO = "info"


class EvidenceCollector(enum.Enum):
    CONNECTOR = "connector"
    AGENT = "agent"
    MANUAL = "manual"
    SCANNER = "scanner"


class PluginType(enum.Enum):
    CONNECTOR = "connector"
    SCANNER = "scanner"
    NOTIFIER = "notifier"
    PACK = "pack"
    REPORT_TEMPLATE = "report-template"


class PluginProtocol(enum.Enum):
    V1 = "v1"


@dataclass
class Organisation:
    id: str = field(default_factory=uuid7)
    name: str = ""
    slug: str = ""
    region: str = "IN"
    settings: dict[str, Any] = field(default_factory=dict)
    status: OrganisationStatus = OrganisationStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Entity:
    id: str = field(default_factory=uuid7)
    organisation_id: str = ""
    name: str = ""
    type: EntityType = EntityType.LEGAL_ENTITY
    parent_entity_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class User:
    id: str = field(default_factory=uuid7)
    email: str = ""
    name: str = ""
    avatar_url: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Membership:
    id: str = field(default_factory=uuid7)
    user_id: str = ""
    organisation_id: str = ""
    role: str = ""  # admin, compliance_manager, control_owner, contributor, executive, auditor
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Framework:
    id: str = field(default_factory=uuid7)
    code: str = ""  # e.g., "soc2", "iso27001", "dpdp"
    name: str = ""
    version: str = ""
    status: FrameworkStatus = FrameworkStatus.DRAFT
    description: str = ""
    source_url: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Requirement:
    id: str = field(default_factory=uuid7)
    framework_version_id: str = ""
    reference: str = ""  # e.g., "CC6.1", "A.5.1"
    title: str = ""
    text: str = ""  # Our own wording
    category: Optional[str] = None
    parent_id: Optional[str] = None
    references: list[dict[str, str]] = field(default_factory=list)  # [{"source": "...", "clause": "..."}]


@dataclass
class Control:
    id: str = field(default_factory=uuid7)
    code: str = ""  # e.g., "CTRL-ACCESS-002"
    title: str = ""
    description: str = ""
    category: str = ""
    guidance: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ControlMapping:
    id: str = field(default_factory=uuid7)
    control_id: str = ""
    requirement_id: str = ""
    strength: MappingStrength = MappingStrength.FULL
    reviewer_note: str = ""


@dataclass
class EntityFramework:
    id: str = field(default_factory=uuid7)
    entity_id: str = ""
    framework_id: str = ""
    framework_version_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ControlImplementation:
    id: str = field(default_factory=uuid7)
    entity_id: str = ""
    control_id: str = ""
    status: ControlStatus = ControlStatus.NOT_STARTED
    owner_id: Optional[str] = None
    not_applicable_reason: Optional[str] = None
    next_review_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Exception:
    id: str = field(default_factory=uuid7)
    control_implementation_id: str = ""
    reason: str = ""
    approver_id: str = ""
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Plugin:
    id: str = field(default_factory=uuid7)
    plugin_id: str = ""  # e.g., "github"
    version: str = ""
    type: PluginType = PluginType.CONNECTOR
    protocol: PluginProtocol = PluginProtocol.V1
    manifest: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PluginInstall:
    id: str = field(default_factory=uuid7)
    organisation_id: str = ""
    plugin_id: str = ""
    plugin_version: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    status: str = "active"  # active, disabled, error
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PluginCredential:
    id: str = field(default_factory=uuid7)
    plugin_install_id: str = ""
    encrypted_secret: str = ""
    key_id: str = ""
    last_rotated_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CollectionRun:
    id: str = field(default_factory=uuid7)
    plugin_install_id: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: Optional[datetime] = None
    status: str = "running"  # running, completed, failed
    records_collected: int = 0
    records_failed: int = 0
    error: Optional[str] = None


@dataclass
class EvidenceRecord:
    id: str = field(default_factory=uuid7)
    organisation_id: str = ""
    source_plugin: str = ""
    plugin_version: str = ""
    collector: EvidenceCollector = EvidenceCollector.CONNECTOR
    check: str = ""
    subject: str = ""
    result: EvidenceResult = EvidenceResult.INFO
    collected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None
    data: dict[str, Any] = field(default_factory=dict)
    hash: str = ""
    prev_hash: str = ""
    linked_controls: list[str] = field(default_factory=list)


@dataclass
class EvidenceFile:
    id: str = field(default_factory=uuid7)
    evidence_id: str = ""
    object_store_key: str = ""
    size: int = 0
    content_type: str = ""
    scan_status: str = "pending"  # pending, clean, infected, error


@dataclass
class EvidenceLink:
    id: str = field(default_factory=uuid7)
    evidence_id: str = ""
    control_implementation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ControlTest:
    id: str = field(default_factory=uuid7)
    control_id: str = ""
    title: str = ""
    schedule: str = "daily"  # hourly, daily, weekly, monthly
    inputs: list[dict[str, Any]] = field(default_factory=list)
    condition: str = ""  # CEL expression
    severity: str = "medium"  # low, medium, high, critical
    on_fail_task: str = ""
    on_fail_notify: list[str] = field(default_factory=list)
    exception_max_days: int = 30
    exception_requires_approval: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TestResult:
    id: str = field(default_factory=uuid7)
    control_test_id: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    result: EvidenceResult = EvidenceResult.INFO
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data_used: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
