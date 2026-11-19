# SPDX-License-Identifier: Apache-2.0
"""Rules Engine - evaluates control tests against evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import ControlTest, TestResult, TestSeverity, TestRunResult, TestInput
from .cel_evaluator import CELEvaluator, EvaluationContext
from sampati_ledger.service import EvidenceLedger


class RulesEngine:
    """Evaluates control tests against collected evidence."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.ledger = EvidenceLedger(session)
        self.evaluator = CELEvaluator()

    async def evaluate_test(
        self,
        test: ControlTest,
        organisation_id: str,
    ) -> TestRunResult:
        """Evaluate a single control test."""
        # Compile the CEL expression
        try:
            compiled = self.evaluator.compile(test.condition)
        except ValueError as e:
            return TestRunResult(
                test_id=test.id,
                result=TestResult.ERROR,
                error=f"CEL compilation failed: {e}",
            )

        # Fetch evidence for all inputs
        evidence = {}
        evidence_ids = []
        
        for input_def in test.inputs:
            records = await self.ledger.get_records(
                organisation_id=organisation_id,
                check=input_def.evidence_check,
                limit=1000,
            )
            
            # Apply filters
            filtered = []
            for r in records:
                match = True
                for k, v in input_def.filters.items():
                    if k == "result" and r.result != v:
                        match = False
                        break
                    # Add more filter types as needed
                if match:
                    filtered.append(r)
            
            evidence[input_def.evidence_check] = [
                {
                    "id": r.id,
                    "result": r.result.value,
                    "subject": r.subject,
                    "data": r.data,
                    "collected_at": r.collected_at.isoformat(),
                }
                for r in filtered
            ]
            evidence_ids.extend([r.id for r in filtered])

        # Create evaluation context
        context = EvaluationContext(
            evidence=evidence,
            now=datetime.now(timezone.utc),
        )

        # Evaluate
        try:
            result = self.evaluator.evaluate(compiled, context)
            
            # Convert result to boolean
            if isinstance(result, bool):
                passed = result
            elif isinstance(result, (int, float)):
                passed = bool(result)
            else:
                passed = False
            
            return TestRunResult(
                test_id=test.id,
                result=TestResult.PASS if passed else TestResult.FAIL,
                evidence_ids=evidence_ids,
                data_used=evidence,
            )
            
        except ValueError as e:
            return TestRunResult(
                test_id=test.id,
                result=TestResult.ERROR,
                error=str(e),
            )

    async def run_scheduled_tests(
        self,
        organisation_id: str,
        schedule: str,
    ) -> list[TestRunResult]:
        """Run all tests for a given schedule."""
        # In production, this would query tests from database
        # For now, return empty list
        return []

    def validate_test(self, test: ControlTest) -> list[str]:
        """Validate a control test definition."""
        errors = []
        
        if not test.id:
            errors.append("test id is required")
        if not test.control_id:
            errors.append("control_id is required")
        if not test.condition:
            errors.append("condition (CEL expression) is required")
        if test.schedule not in ("hourly", "daily", "weekly", "monthly"):
            errors.append(f"invalid schedule: {test.schedule}")
        
        # Validate CEL syntax
        cel_errors = self.evaluator.validate_expression(test.condition)
        errors.extend(cel_errors)
        
        return errors


# 10 Starter Tests for MVP
STARTER_TESTS = [
    ControlTest(
        id="TEST-MFA-001",
        control_id="CTRL-ACCESS-002",
        title="Multi-factor authentication enforced for all active users",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="idp_user_mfa_status"),
        ],
        condition="""
            evidence.filter(e, e.data.active == true).all(e, e.data.mfa_enabled == true)
        """,
        severity=TestSeverity.HIGH,
        on_fail=OnFailConfig(
            task="Enable multi-factor authentication for the listed users",
            notify=["control_owner"],
            escalate_days=7,
        ),
        exceptions=ExceptionConfig(max_days=30, requires_approval=True),
    ),
    ControlTest(
        id="TEST-MFA-002",
        control_id="CTRL-ACCESS-001",
        title="MFA required for administrative access",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="idp_admin_mfa_status"),
        ],
        condition="""
            evidence.filter(e, e.data.is_admin == true).all(e, e.data.mfa_enabled == true)
        """,
        severity=TestSeverity.CRITICAL,
    ),
    ControlTest(
        id="TEST-ENCRYPTION-001",
        control_id="CTRL-DATA-001",
        title="Encryption at rest enabled for all data stores",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="cloud_encryption_at_rest"),
        ],
        condition="""
            evidence.all(e, e.result == "pass")
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-ENCRYPTION-002",
        control_id="CTRL-DATA-002",
        title="Encryption in transit (TLS 1.2+) for all endpoints",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="tls_version_check"),
        ],
        condition="""
            evidence.all(e, e.data.tls_version >= "1.2")
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-BRANCH-PROTECTION-001",
        control_id="CTRL-CODE-001",
        title="Branch protection enabled for all production repositories",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="branch_protection_enabled"),
        ],
        condition="""
            evidence.all(e, e.result == "pass")
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-REQUIRED-REVIEWS-001",
        control_id="CTRL-CODE-002",
        title="Required PR reviews (>=2) for production branches",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="branch_protection_enabled"),
        ],
        condition="""
            evidence.all(e, e.data.required_reviews >= 2)
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-SECRET-SCANNING-001",
        control_id="CTRL-CODE-005",
        title="Secret scanning enabled for all repositories",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="secret_scanning_enabled"),
        ],
        condition="""
            evidence.all(e, e.result == "pass")
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-DEPENDABOT-001",
        control_id="CTRL-CODE-006",
        title="Dependabot alerts enabled for all repositories",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="dependabot_enabled"),
        ],
        condition="""
            evidence.all(e, e.result == "pass")
        """,
        severity=TestSeverity.MEDIUM,
    ),
    ControlTest(
        id="TEST-SUSPENDED-USERS-001",
        control_id="CTRL-ACCESS-003",
        title="No suspended users with active access",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="suspended_users"),
        ],
        condition="""
            evidence.all(e, e.data.suspended_count == 0)
        """,
        severity=TestSeverity.HIGH,
    ),
    ControlTest(
        id="TEST-ADMIN-COUNT-001",
        control_id="CTRL-ACCESS-004",
        title="Admin count within approved threshold",
        schedule="daily",
        inputs=[
            TestInput(evidence_check="admin_privileges"),
        ],
        condition="""
            evidence.all(e, e.data.admin_count <= 5)
        """,
        severity=TestSeverity.MEDIUM,
    ),
]
