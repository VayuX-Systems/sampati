# SPDX-License-Identifier: Apache-2.0
"""Evidence service for managing evidence records."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from sampati_core_domain.models import EvidenceRecord as DBEvidenceRecord, EvidenceCollector, EvidenceResult
from sampati_ledger.service import EvidenceLedger
from sampati_ledger.models import EvidenceRecord, EvidenceCollector, EvidenceResult


class EvidenceService:
    """Service for managing evidence records through the ledger."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.ledger = EvidenceLedger(session)

    async def create_evidence(
        self,
        organisation_id: str,
        source_plugin: str,
        plugin_version: str,
        collector: str,
        check: str,
        subject: str,
        result: str,
        data: dict,
        valid_until_days: int | None = None,
        linked_controls: list[str] | None = None,
    ) -> EvidenceRecord:
        """Create a new evidence record."""
        valid_until = None
        if valid_until_days:
            valid_until = datetime.now(timezone.utc) + timedelta(days=valid_until_days)
        
        return await self.ledger.append(
            organisation_id=organisation_id,
            source_plugin=source_plugin,
            plugin_version=plugin_version,
            collector=EvidenceCollector(collector),
            check=check,
            subject=subject,
            result=EvidenceResult(result),
            data=data,
            valid_until=valid_until,
            linked_controls=linked_controls,
        )

    async def list_evidence(
        self,
        organisation_id: str,
        limit: int = 20,
        offset: int = 0,
        check: str | None = None,
        result: str | None = None,
        since: str | None = None,
    ) -> list[EvidenceRecord]:
        """List evidence records with optional filters."""
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            except ValueError:
                pass
        
        return await self.ledger.get_records(
            organisation_id=organisation_id,
            limit=limit,
            offset=offset,
            check=check,
            result=EvidenceResult(result) if result else None,
            since=since_dt,
        )

    async def verify_chain(self, organisation_id: str) -> tuple[bool, list[str]]:
        """Verify the integrity of the evidence ledger hash chain."""
        return await self.ledger.verify_chain(organisation_id)

    async def get_latest_hash(self, organisation_id: str) -> str:
        """Get the latest hash in the chain."""
        return await self.ledger.get_latest_hash(organisation_id)

    async def get_stale_evidence(
        self,
        organisation_id: str,
        threshold_days: int = 90,
    ) -> list[EvidenceRecord]:
        """Get evidence records that have expired."""
        return await self.ledger.get_stale_evidence(organisation_id, threshold_days)

    async def get_evidence(self, evidence_id: str, organisation_id: str) -> Optional[EvidenceRecord]:
        """Get a single evidence record by ID."""
        return await self.ledger.get_record(evidence_id, organisation_id)
