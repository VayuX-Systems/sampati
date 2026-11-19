from datetime import datetime, timezone, timedelta
# SPDX-License-Identifier: Apache-2.0
"""Tests for Evidence Ledger."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sampati_core_domain.models import Organisation, User, Membership, BuiltInRole
from sampati_ledger.service import EvidenceLedger
from sampati_ledger.models import EvidenceRecord, EvidenceCollector, EvidenceResult


@pytest.fixture
async def test_org(db_session: AsyncSession) -> str:
    """Create a test organisation."""
    org_id = str(uuid.uuid4())
    org = Organisation(
        id=org_id,
        name="Test Org",
        slug=f"test-org-{uuid.uuid4().hex[:8]}",
        region="IN",
    )
    db_session.add(org)
    await db_session.commit()
    return org_id


@pytest.fixture
async def test_user(db_session: AsyncSession, test_org: str) -> str:
    """Create a test user."""
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=f"test-{uuid.uuid4().hex[:8]}@example.com",
        name="Test User",
    )
    db_session.add(user)
    
    membership = Membership(
        id=str(uuid.uuid4()),
        user_id=user_id,
        organisation_id=test_org,
        role=BuiltInRole.ADMIN.value,
    )
    db_session.add(membership)
    await db_session.commit()
    return user_id


class TestEvidenceLedger:
    """Tests for EvidenceLedger service."""

    @pytest.mark.asyncio
    async def test_append_creates_record_with_hash(self, db_session: AsyncSession, test_org: str):
        """Test that appending creates a record with proper hash chain."""
        ledger = EvidenceLedger(db_session)
        
        record = await ledger.append(
            organisation_id=test_org,
            source_plugin="test-plugin",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check="test_check",
            subject="test_subject",
            result=EvidenceResult.PASS,
            data={"key": "value"},
            linked_controls=["CTRL-001"],
        )
        
        assert record.id is not None
        assert record.organisation_id == test_org
        assert record.hash.startswith("sha256:")
        assert record.prev_hash == ""  # First record has no previous hash
        assert record.linked_controls == ["CTRL-001"]

    @pytest.mark.asyncio
    async def test_second_record_links_to_first(self, db_session: AsyncSession, test_org: str):
        """Test that second record's prev_hash equals first record's hash."""
        ledger = EvidenceLedger(db_session)
        
        # Create first record
        record1 = await ledger.append(
            organisation_id=test_org,
            source_plugin="test-plugin",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check="check_1",
            subject="subject_1",
            result=EvidenceResult.PASS,
            data={"num": 1},
        )
        
        # Create second record
        record2 = await ledger.append(
            organisation_id=test_org,
            source_plugin="test-plugin",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check="check_2",
            subject="subject_2",
            result=EvidenceResult.FAIL,
            data={"num": 2},
        )
        
        # Second record's prev_hash should equal first record's hash
        assert record2.prev_hash == record1.hash
        
        # Both hashes should be valid
        assert record1.verify_hash("")
        assert record2.verify_hash(record1.hash)

    @pytest.mark.asyncio
    async def test_verify_chain_valid(self, db_session: AsyncSession, test_org: str):
        """Test that a valid chain passes verification."""
        ledger = EvidenceLedger(db_session)
        
        # Create a few records
        for i in range(5):
            await ledger.append(
                organisation_id=test_org,
                source_plugin="test-plugin",
                plugin_version="1.0.0",
                collector=EvidenceCollector.CONNECTOR,
                check=f"check_{i}",
                subject=f"subject_{i}",
                result=EvidenceResult.PASS,
                data={"index": i},
            )
        
        is_valid, errors = await ledger.verify_chain(test_org)
        assert is_valid is True
        assert errors == []

    @pytest.mark.asyncio
    async def test_verify_chain_detects_tampering(self, db_session: AsyncSession, test_org: str):
        """Test that verification detects tampered records."""
        ledger = EvidenceLedger(db_session)
        
        # Create records
        for i in range(3):
            await ledger.append(
                organisation_id=test_org,
                source_plugin="test-plugin",
                plugin_version="1.0.0",
                collector=EvidenceCollector.CONNECTOR,
                check=f"check_{i}",
                subject=f"subject_{i}",
                result=EvidenceResult.PASS,
                data={"index": i},
            )
        
        # Get the middle record and tamper with it in the database
        from sampati_core_domain.models import EvidenceRecord as DBEvidenceRecord
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(EvidenceRecord).where(
                EvidenceRecord.organisation_id == test_org
            ).order_by(EvidenceRecord.collected_at.asc()).offset(1).limit(1)
        )
        middle_record = result.scalar_one()
        
        # Tamper: change the data
        middle_record.data = {"tampered": True}
        await db_session.commit()
        
        # Verify should fail
        is_valid, errors = await ledger.verify_chain(test_org)
        assert is_valid is False
        assert len(errors) > 0
        assert any("hash mismatch" in e for e in errors)

    @pytest.mark.asyncio
    async def test_get_stale_evidence(self, db_session: AsyncSession, test_org: str):
        """Test getting stale (expired) evidence."""
        ledger = EvidenceLedger(db_session)
        
        # Create expired record
        await ledger.append(
            organisation_id=test_org,
            source_plugin="test-plugin",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check="expired_check",
            subject="expired_subject",
            result=EvidenceResult.PASS,
            data={},
            valid_until=datetime.now(timezone.utc) - timedelta(days=1),
        )
        
        # Create valid record
        await ledger.append(
            organisation_id=test_org,
            source_plugin="test-plugin",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check="valid_check",
            subject="valid_subject",
            result=EvidenceResult.PASS,
            data={},
            valid_until=datetime.now(timezone.utc) + timedelta(days=30),
        )
        
        stale = await ledger.get_stale_evidence(test_org, threshold_days=90)
        assert len(stale) == 1
        assert stale[0].check == "expired_check"

    @pytest.mark.asyncio
    async def test_isolation_between_orgs(self, db_session: AsyncSession):
        """Test that organisations cannot see each other's evidence."""
        ledger = EvidenceLedger(db_session)
        
        # Create two organisations
        org_a = str(uuid.uuid4())
        org_b = str(uuid.uuid4())
        
        org_a_obj = Organisation(id=org_a, name="Org A", slug="org-a", region="IN")
        org_b_obj = Organisation(id=org_b, name="Org B", slug="org-b", region="IN")
        db_session.add_all([org_a_obj, org_b_obj])
        await db_session.commit()
        
        # Add evidence to Org A
        await ledger.append(
            organisation_id=org_a,
            source_plugin="test",
            plugin_version="1.0",
            collector=EvidenceCollector.CONNECTOR,
            check="check_a",
            subject="subject_a",
            result=EvidenceResult.PASS,
            data={},
        )
        
        # Add evidence to Org B
        await ledger.append(
            organisation_id=org_b,
            source_plugin="test",
            plugin_version="1.0",
            collector=EvidenceCollector.CONNECTOR,
            check="check_b",
            subject="subject_b",
            result=EvidenceResult.PASS,
            data={},
        )
        
        # Query as Org A - should only see Org A's records
        records_a = await ledger.get_records(org_a)
        assert len(records_a) == 1
        assert records_a[0].check == "check_a"
        
        # Query as Org B - should only see Org B's records
        records_b = await ledger.get_records(org_b)
        assert len(records_b) == 1
        assert records_b[0].check == "check_b"
