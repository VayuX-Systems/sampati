# SPDX-License-Identifier: Apache-2.0
"""Rules engine models."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class TestSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TestResult(enum.Enum):
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
    id: str = field(default_factory=lambda: str(uuid4()))
    control_id: str = ""
    title: str = ""
    schedule: str = "daily"  # hourly, daily, weekly, monthly
    inputs: list[TestInput] = field(default_factory=list)
    condition: str = ""  # CEL expression
    severity: TestSeverity = TestSeverity.MEDIUM
    on_fail: OnFailConfig = field(default_factory=OnFailConfig)
    exceptions: ExceptionConfig = field(default_factory=ExceptionConfig)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TestRunResult:
    test_id: str
    result: TestResult
    evidence_ids: list[str] = field(default_factory=list)
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data_used: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
