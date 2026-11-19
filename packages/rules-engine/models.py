# SPDX-License-Identifier: Apache-2.0
"""Rules engine models and evaluator for control tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TestSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TestResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class TestInput:
    evidence_check: str
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass
class OnFailConfig:
    task: str = ""
    notify: list[str] = field(default_factory=list)
    escalate_days: int = 7


@dataclass
class ExceptionConfig:
    max_days: int = 30
    requires_approval: bool = True


@dataclass
class ControlTest:
    id: str
    control_id: str
    title: str
    schedule: str  # hourly, daily, weekly, monthly
    inputs: list[TestInput] = field(default_factory=list)
    condition: str = ""  # CEL expression
    severity: TestSeverity = TestSeverity.MEDIUM
    on_fail: OnFailConfig = field(default_factory=OnFailConfig)
    exceptions: ExceptionConfig = field(default_factory=ExceptionConfig)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TestRunResult:
    control_test_id: str
    result: TestResult
    evidence_ids: list[str] = field(default_factory=list)
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data_used: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class RulesEngine:
    """
    Evaluates control tests using CEL expressions.

    In the alpha, this is a stub. Production implementation will use
    a CEL interpreter (cel-py or similar) with a sandboxed environment.
    """

    def __init__(self) -> None:
        pass

    def evaluate(self, test: ControlTest, evidence: dict[str, list[dict[str, Any]]]) -> TestRunResult:
        """
        Evaluate a control test against collected evidence.

        Args:
            test: The control test to evaluate
            evidence: Dict mapping evidence_check name to list of evidence records

        Returns:
            TestRunResult with the evaluation outcome
        """
        # TODO: Implement CEL evaluation with cel-py
        # For now, return a placeholder result
        return TestRunResult(
            control_test_id=test.id,
            result=TestResult.ERROR,
            error="CEL evaluation not implemented in alpha",
        )

    def validate_test(self, test: ControlTest) -> list[str]:
        """Validate a control test definition. Returns list of errors."""
        errors = []
        if not test.id:
            errors.append("test id is required")
        if not test.control_id:
            errors.append("control_id is required")
        if not test.condition:
            errors.append("condition (CEL expression) is required")
        if test.schedule not in ("hourly", "daily", "weekly", "monthly"):
            errors.append(f"invalid schedule: {test.schedule}")
        # TODO: Validate CEL syntax
        return errors
