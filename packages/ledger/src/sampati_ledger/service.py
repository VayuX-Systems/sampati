# SPDX-License-Identifier: Apache-2.0
"""Evidence ledger service with hash chain and database persistence."""

from __future__ import annotations

import hashlib
import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from typing import Any, AsyncGenerator, Optional
from uuid import uuid4

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from sampati_core_domain.models import EvidenceRecord as DBEvidenceRecord, Organisation
from .models import EvidenceRecord, EvidenceCollector, EvidenceResult, LedgerVerificationError


class EvidenceLedger:
    """
    Append-only evidence ledger with SHA-256 hash chain.
    
    Each record's hash includes the previous record's hash, forming an 
    immutable chain. Any tampering breaks the chain.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def append(
        self,
        organisation_id: str,
        source_plugin: str,
        plugin_version: str,
        collector: EvidenceCollector,
        check: str,
        subject: str,
        result: EvidenceResult,
        data: dict[str, Any],
        valid_until: Optional[datetime] = None,
        linked_controls: Optional[list[str]] = None,
    ) -> EvidenceRecord:
        """Append a new evidence record to the ledger."""
        
        # Get the last hash for this organisation
        prev_hash = await self._get_last_hash(organisation_id)
        
        # Create the record
        record = EvidenceRecord(
            id=str(uuid4()),
            organisation_id=organisation_id,
            source_plugin=source_plugin,
            plugin_version=plugin_version,
            collector=collector,
            check=check,
            subject=subject,
            result=result,
            collected_at=datetime.now(timezone.utc),
            valid_until=valid_until,
            data=data,
            prev_hash=prev_hash,
            linked_controls=linked_controls or [],
        )
        
        # Compute hash
        record.hash = record.compute_hash(prev_hash)
        
        # Persist to database
        db_record = DBEvidenceRecord(
            id=record.id,
            organisation_id=record.organisation_id,
            source_plugin=record.source_plugin,
            plugin_version=record.plugin_version,
            collector=record.collector.value,
            check=record.check,
            subject=record.subject,
            result=record.result.value,
            collected_at=record.collected_at,
            valid_until=record.valid_until,
            data=record.data,
            hash=record.hash,
            prev_hash=record.prev_hash,
            linked_controls=record.linked_controls,
        )
        
        self.session.add(db_record)
        await self.session.flush()
        
        return record

    async def _get_last_hash(self, organisation_id: str) -> str:
        """Get the hash of the most recent record for an organisation."""
        stmt = select(DBEvidenceRecord.hash).where(
            DBEvidenceRecord.organisation_id == organisation_id
        ).order_by(DBEvidenceRecord.collected_at.desc()).limit(1)
        
        result = await self.session.execute(stmt)
        last_hash = result.scalar_one_or_none()
        return last_hash or ""

    async def get_record(self, record_id: str, organisation_id: str) -> Optional[EvidenceRecord]:
        """Get a single evidence record by ID."""
        stmt = select(DBEvidenceRecord).where(
            DBEvidenceRecord.id == record_id,
            DBEvidenceRecord.organisation_id == organisation_id
        )
        result = await self.session.execute(stmt)
        db_record = result.scalar_one_or_none()
        
        if not db_record:
            return None
        
        return self._to_evidence_record(db_record)

    async def get_records(
        self,
        organisation_id: str,
        limit: int = 100,
        offset: int = 0,
        check: Optional[str] = None,
        result: Optional[EvidenceResult] = None,
        since: Optional[datetime] = None,
    ) -> list[EvidenceRecord]:
        """Get evidence records with optional filters."""
        stmt = select(DBEvidenceRecord).where(
            DBEvidenceRecord.organisation_id == organisation_id
        ).order_by(DBEvidenceRecord.collected_at.desc()).limit(limit).offset(offset)
        
        if check:
            stmt = stmt.where(DBEvidenceRecord.check == check)
        if result:
            stmt = stmt.where(DBEvidenceRecord.result == result.value)
        if since:
            stmt = stmt.where(DBEvidenceRecord.collected_at >= since)
        
        result = await self.session.execute(stmt)
        db_records = result.scalars().all()
        
        return [self._to_evidence_record(r) for r in db_records]

    async def verify_chain(self, organisation_id: str) -> tuple[bool, list[str]]:
        """
        Verify the integrity of the entire hash chain for an organisation.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Get all records in chronological order
        stmt = select(DBEvidenceRecord).where(
            DBEvidenceRecord.organisation_id == organisation_id
        ).order_by(DBEvidenceRecord.collected_at.asc())
        
        result = await self.session.execute(stmt)
        records = result.scalars().all()
        
        if not records:
            return True, []
        
        prev_hash = ""
        for i, db_record in enumerate(records):
            evidence = self._to_evidence_record(db_record)
            
            # Verify prev_hash matches
            if evidence.prev_hash != prev_hash:
                errors.append(
                    f"Record {i} ({evidence.id}): prev_hash mismatch. "
                    f"Expected {prev_hash}, got {evidence.prev_hash}"
                )
            
            # Verify record's own hash
            expected_hash = evidence.compute_hash(prev_hash)
            if evidence.hash != expected_hash:
                errors.append(
                    f"Record {i} ({evidence.id}): hash mismatch. "
                    f"Expected {expected_hash}, got {evidence.hash}"
                )
            
            prev_hash = evidence.hash
        
        return len(errors) == 0, errors

    async def get_latest_hash(self, organisation_id: str) -> str:
        """Get the latest hash in the chain."""
        return await self._get_last_hash(organisation_id)

    async def get_stale_evidence(
        self,
        organisation_id: str,
        threshold_days: int = 90,
    ) -> list[EvidenceRecord]:
        """Get evidence records that have expired (stale)."""
        threshold = datetime.now(timezone.utc) - timedelta(days=threshold_days)
        
        stmt = select(DBEvidenceRecord).where(
            DBEvidenceRecord.organisation_id == organisation_id,
            DBEvidenceRecord.valid_until.isnot(None),
            DBEvidenceRecord.valid_until < datetime.now(timezone.utc),
        ).order_by(DBEvidenceRecord.valid_until.asc())
        
        result = await self.session.execute(stmt)
        db_records = result.scalars().all()
        
        return [self._to_evidence_record(r) for r in db_records]

    async def count_records(self, organisation_id: str) -> int:
        """Count total records for an organisation."""
        stmt = select(func.count()).select_from(DBEvidenceRecord).where(
            DBEvidenceRecord.organisation_id == organisation_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    def _to_evidence_record(self, db_record: DBEvidenceRecord) -> EvidenceRecord:
        """Convert database record to domain model."""
        return EvidenceRecord(
            id=str(db_record.id),
            organisation_id=str(db_record.organisation_id),
            source_plugin=db_record.source_plugin,
            plugin_version=db_record.plugin_version,
            collector=EvidenceCollector(db_record.collector),
            check=db_record.check,
            subject=db_record.subject,
            result=EvidenceResult(db_record.result),
            collected_at=db_record.collected_at,
            valid_until=db_record.valid_until,
            data=db_record.data,
            hash=db_record.hash,
            prev_hash=db_record.prev_hash,
            linked_controls=db_record.linked_controls,
        )


@asynccontextmanager
async def get_ledger(session: AsyncSession) -> AsyncGenerator[EvidenceLedger, None]:
    """Context manager for EvidenceLedger."""
    ledger = EvidenceLedger(session)
    try:
        yield ledger
        await session.commit()
    except Exception:
        await session.rollback()
        raise
