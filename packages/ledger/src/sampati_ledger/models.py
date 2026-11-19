# SPDX-License-Identifier: Apache-2.0
"""Evidence ledger models."""

from __future__ import annotations

import enum
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


class EvidenceCollector(str, enum.Enum):
    CONNECTOR = "connector"
    AGENT = "agent"
    MANUAL = "manual"
    SCANNER = "scanner"


class EvidenceResult(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    INFO = "info"


@dataclass
class EvidenceRecord:
    """Immutable evidence record with hash chain linkage."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
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
    
    def to_canonical_dict(self, prev_hash: str = "") -> dict[str, Any]:
        """Create canonical dict for hashing (sorted keys, deterministic)."""
        return {
            "id": self.id,
            "organisation_id": self.organisation_id,
            "source_plugin": self.source_plugin,
            "plugin_version": self.plugin_version,
            "collector": self.collector.value,
            "check": self.check,
            "subject": self.subject,
            "result": self.result.value,
            "collected_at": self.collected_at.isoformat().replace("+00:00", "Z"),
            "valid_until": self.valid_until.isoformat().replace("+00:00", "Z") if self.valid_until else None,
            "data": self.data,
            "prev_hash": prev_hash,
            "linked_controls": self.linked_controls,
        }
    
    def compute_hash(self, prev_hash: str = "") -> str:
        """Compute SHA-256 hash of this record + previous hash."""
        canonical = json.dumps(self.to_canonical_dict(prev_hash), sort_keys=True, separators=(",", ":"))
        content = f"{canonical}{prev_hash}".encode()
        return f"sha256:{hashlib.sha256(content).hexdigest()}"
    
    def verify_hash(self, prev_hash: str = "") -> bool:
        """Verify this record's hash matches computed hash."""
        expected = self.compute_hash(prev_hash)
        return self.hash == expected


class LedgerVerificationError(Exception):
    """Raised when ledger verification fails."""
    pass
