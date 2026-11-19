# SPDX-License-Identifier: Apache-2.0
"""Framework, control, and crosswalk models."""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


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


@dataclass
class Framework:
    """Compliance framework."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    code: str = ""
    name: str = ""
    version: str = ""
    status: FrameworkStatus = FrameworkStatus.DRAFT
    description: str = ""
    source_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Requirement:
    """Framework requirement."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    framework_version_id: str = ""
    reference: str = ""  # e.g., "CC6.1", "A.5.1"
    title: str = ""
    text: str = ""  # Our own wording
    category: str | None = None
    parent_id: str | None = None
    references: list[dict[str, str]] = field(default_factory=list)


@dataclass
class Control:
    """Unified control (implements once, complies many)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    code: str = ""  # e.g., "CTRL-ACCESS-002"
    title: str = ""
    description: str = ""
    category: str = ""
    guidance: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ControlMapping:
    """Mapping between a control and a framework requirement."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    control_id: str = ""
    requirement_id: str = ""
    strength: MappingStrength = MappingStrength.FULL
    reviewer_note: str = ""


@dataclass
class EntityFramework:
    """Framework selection for an entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    framework_id: str = ""
    framework_version_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ControlImplementation:
    """Implementation status of a control for an entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    control_id: str = ""
    status: ControlStatus = ControlStatus.NOT_STARTED
    owner_id: str | None = None
    not_applicable_reason: str | None = None
    next_review_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Exception:
    """Time-limited exception for a control."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    control_implementation_id: str = ""
    reason: str = ""
    approver_id: str = ""
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
