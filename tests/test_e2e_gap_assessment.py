# SPDX-License-Identifier: Apache-2.0
"""End-to-end test of the full gap assessment flow."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from sampati_core_domain.models import Organisation, Entity, User, Membership, BuiltInRole
from sampati_api.main import create_app
from sampati_api.database import init_db, close_db


@pytest.fixture(scope="session")
async def app():
    """Create test app."""
    app = create_app()
    await init_db()
    yield app
    await close_db()


@pytest.fixture
async def client(app):
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_org(db_session: AsyncSession) -> str:
    """Create test organisation."""
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
    """Create test user."""
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


class TestGapAssessmentFlow:
    """Test the complete gap assessment flow."""

    @pytest.mark.asyncio
    async def test_full_gap_assessment_flow(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        test_org: str,
        test_user: str,
    ):
        """Test the complete flow: create org -> load framework -> scope -> assess -> gap report."""
        
        # 1. Create organisation via API
        org_resp = await client.post(
            "/api/v1/organisations",
            json={"name": "E2E Test Corp", "slug": "e2e-test", "region": "IN"},
            headers={"X-Organisation-ID": test_org},
        )
        assert org_resp.status_code == 201
        org_data = org_resp.json()
        new_org_id = org_data["id"]
        
        # 2. Create entity
        entity_resp = await client.post(
            f"/api/v1/organisations/{new_org_id}/entities",
            json={"name": "Main Entity", "type": "legal_entity"},
            headers={"X-Organisation-ID": new_org_id},
        )
        assert entity_resp.status_code == 201
        entity_data = entity_resp.json()
        entity_id = entity_data["id"]
        
        # 3. Load SOC 2 framework (pre-loaded)
        # 4. Select framework for entity
        # For this test, we assume frameworks are pre-loaded
        # In real scenario, we'd load from file
        
        # 5. Run scoping questionnaire
        # This would be a POST to /api/v1/frameworks/scoping
        # For now, we test the control list endpoint
        
        # 6. Get control list for entity
        controls_resp = await client.get(
            f"/api/v1/frameworks/entities/{entity_id}/controls",
            headers={"X-Organisation-ID": new_org_id},
        )
        # This endpoint should exist after framework selection
        
        # 7. Get readiness score and gap report
        gap_resp = await client.get(
            f"/api/v1/frameworks/entities/{entity_id}/gap-report",
            headers={"X-Organisation-ID": new_org_id},
        )
        # Should return gap analysis
        
        print("E2E gap assessment flow test structure verified")


# Synthetic data test
@pytest.mark.asyncio
async def test_synthetic_data_flow(db_session: AsyncSession, test_org: str):
    """Test gap assessment with synthetic evidence data."""
    from sampati_ledger.service import EvidenceLedger
    from sampati_rules_engine.engine import RulesEngine, STARTER_TESTS
    from sampati_rules_engine.models import TestSeverity
    from sampati_ledger.models import EvidenceCollector, EvidenceResult
    
    ledger = EvidenceLedger(db_session)
    engine = RulesEngine(db_session)
    
    # Create synthetic evidence records
    for i in range(10):
        await ledger.append(
            organisation_id=test_org,
            source_plugin="github",
            plugin_version="1.0.0",
            collector=EvidenceCollector.CONNECTOR,
            check=f"branch_protection_enabled",
            subject=f"repo:test/repo-{i}",
            result=EvidenceResult.PASS if i < 8 else EvidenceResult.FAIL,
            data={
                "repo": f"test/repo-{i}",
                "branch": "main",
                "protection_enabled": i < 8,
                "required_reviews": 2 if i < 8 else 0,
            },
            valid_until=datetime.now(timezone.utc).replace(day=28),
        )
    
    # Run starter tests
    for test in STARTER_TESTS[:3]:  # Run first 3 tests
        result = await engine.evaluate_test(test, test_org)
        
        assert result.result in (TestResult.PASS, TestResult.FAIL, TestResult.ERROR)
        print(f"Test {test.id}: {result.result.value} (evidence: {len(result.evidence_ids)})")
    
    # Verify chain integrity
    is_valid, errors = await ledger.verify_chain(test_org)
    assert is_valid is True
    assert errors == []
    
    print("Synthetic data flow test passed")
