# SPDX-License-Identifier: Apache-2.0
"""Evidence ledger with hash chain for tamper-evident storage."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class LedgerRecord:
    """Single record in the append-only evidence ledger."""

    id: str = field(default_factory=lambda: str(uuid4()))
    organisation_id: str = ""
    source_plugin: str = ""
    plugin_version: str = ""
    collector: str = ""  # connector, agent, manual, scanner
    check: str = ""
    subject: str = ""
    result: str = ""  # pass, fail, error, info
    collected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: datetime | None = None
    data: dict[str, Any] = field(default_factory=dict)
    hash: str = ""
    prev_hash: str = ""
    linked_controls: list[str] = field(default_factory=list)

    def compute_hash(self, prev_hash: str = "") -> str:
        """Compute SHA-256 hash of this record plus previous hash."""
        # Create deterministic JSON representation
        record_dict = {
            "id": self.id,
            "organisation_id": self.organisation_id,
            "source_plugin": self.source_plugin,
            "plugin_version": self.plugin_version,
            "collector": self.collector,
            "check": self.check,
            "subject": self.subject,
            "result": self.result,
            "collected_at": self.collected_at.isoformat().replace("+00:00", "Z"),
            "valid_until": self.valid_until.isoformat().replace("+00:00", "Z") if self.valid_until else None,
            "data": self.data,
            "prev_hash": prev_hash,
            "linked_controls": self.linked_controls,
        }
        canonical = json.dumps(record_dict, sort_keys=True, separators=(",", ":"))
        content = f"{canonical}{prev_hash}".encode()
        return f"sha256:{hashlib.sha256(content).hexdigest()}"


class EvidenceLedger:
    """
    Append-only evidence ledger with hash chain.

    Each record's hash includes the previous record's hash, forming a chain.
    Tampering with any record breaks the chain.
    """

    def __init__(self) -> None:
        self._records: list[LedgerRecord] = []
        self._last_hash: str = ""

    def append(self, record: LedgerRecord) -> LedgerRecord:
        """Append a record to the ledger, computing its hash."""
        record.prev_hash = self._last_hash
        record.hash = record.compute_hash(self._last_hash)
        self._records.append(record)
        self._last_hash = record.hash
        return record

    def verify_chain(self) -> tuple[bool, list[str]]:
        """
        Verify the integrity of the entire chain.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        prev_hash = ""
        for i, record in enumerate(self._records):
            expected_hash = record.compute_hash(prev_hash)
            if record.hash != expected_hash:
                errors.append(f"Record {i} ({record.id}): hash mismatch (expected {expected_hash}, got {record.hash})")
            if record.prev_hash != prev_hash:
                errors.append(f"Record {i} ({record.id}): prev_hash mismatch (expected {prev_hash}, got {record.prev_hash})")
            prev_hash = record.hash
        return len(errors) == 0, errors

    def get_records(self, organisation_id: str) -> list[LedgerRecord]:
        """Get all records for an organisation."""
        return [r for r in self._records if r.organisation_id == organisation_id]

    def get_latest_hash(self) -> str:
        """Get the latest hash in the chain."""
        return self._last_hash
