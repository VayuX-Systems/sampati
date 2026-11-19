# SPDX-License-Identifier: Apache-2.0
"""Evidence Request domain model."""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


class EvidenceRequestStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class EvidenceRequestPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EvidenceRequest:
    """Request for manual evidence collection."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organisation_id: str = ""
    title: str = ""
    description: str = ""
    requested_by_id: str = ""
    assignee_id: str = ""
    control_implementation_id: Optional[str] = None
    status: EvidenceRequestStatus = EvidenceRequestStatus.PENDING
    priority: EvidenceRequestPriority = EvidenceRequestPriority.MEDIUM
    due_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    evidence_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
