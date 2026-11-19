# SPDX-License-Identifier: Apache-2.0
"""CEL evaluator for control tests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from celpy import Environment
from celpy.cel import celpy


@dataclass
class EvaluationContext:
    """Context for CEL evaluation."""
    evidence: dict[str, list[dict[str, Any]]]
    now: datetime


class CELEvaluator:
    """Evaluates CEL expressions in a sandboxed environment."""

    def __init__(self) -> None:
        # Create CEL environment with standard library
        self.env = Environment()
        
        # Add custom functions if needed
        # self.env.add_function(...)

    def compile(self, expression: str) -> Any:
        """Compile a CEL expression."""
        try:
            return self.env.compile(expression)
        except Exception as e:
            raise ValueError(f"CEL compilation failed: {e}")

    def evaluate(
        self, 
        compiled_expr: Any, 
        context: EvaluationContext
    ) -> Any:
        """Evaluate a compiled CEL expression."""
        try:
            # Create activation with context variables
            activation = self.env.activation_factory().new_activation()
            
            # Add evidence helper function
            def evidence_filter(check: str, filters: dict = None):
                """Filter evidence records."""
                records = context.evidence.get(check, [])
                if filters:
                    filtered = []
                    for r in records:
                        match = True
                        for k, v in filters.items():
                            if k == "result" and r.get("result") != v:
                                match = False
                                break
                            if k == "subject" and v not in r.get("subject", ""):
                                match = False
                                break
                        if match:
                            filtered.append(r)
                    return filtered
                return records
            
            # Add helper functions to activation
            activation.add_function("evidence", evidence_filter)
            
            # Add 'now' variable
            activation.add_variable("now", context.now)
            
            # Evaluate
            result = compiled_expr.evaluate(activation)
            return result
            
        except Exception as e:
            raise ValueError(f"CEL evaluation failed: {e}")

    def validate_expression(self, expression: str) -> list[str]:
        """Validate a CEL expression. Returns list of errors."""
        try:
            self.compile(expression)
            return []
        except Exception as e:
            return [str(e)]
