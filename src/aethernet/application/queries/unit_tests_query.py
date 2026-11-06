"""Immutable read-side request for deterministic test result inspection."""

from dataclasses import dataclass
from enum import StrEnum


class OutcomeFilter(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMED_OUT = "timed_out"


@dataclass(frozen=True, slots=True)
class UnitTestsQuery:
    """Select recorded test evidence without launching a test runner."""

    scope: str = "unit"
    outcome: OutcomeFilter | None = None
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.scope not in ("unit", "integration", "scenario"):
            raise ValueError("scope must be unit, integration or scenario")
        if self.outcome is not None and not isinstance(self.outcome, OutcomeFilter):
            raise TypeError("outcome must be an OutcomeFilter")
        if not 1 <= self.limit <= 500 or self.offset < 0:
            raise ValueError("pagination must use limit 1..500 and nonnegative offset")

    def matches(self, test_path: str, outcome: str) -> bool:
        """Reject paths outside the requested inventory scope."""
        prefix = f"tests/{self.scope}/"
        if not test_path.startswith(prefix):
            return False
        return self.outcome is None or outcome == self.outcome.value
