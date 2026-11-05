"""Typed inventory and result-reporting contracts for local test executors."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class TestOutcome(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMED_OUT = "timed_out"


@dataclass(frozen=True, slots=True)
class TestResult:
    identifier: str
    outcome: TestOutcome
    duration_ms: int
    message: str = ""

    def __post_init__(self) -> None:
        if self.duration_ms < 0:
            raise ValueError("duration must not be negative")


class TestInventoryPort(Protocol):
    def enumerate(self, scope: str) -> tuple[str, ...]: ...


class TestExecutorPort(Protocol):
    """Execute only a validated list of test identifiers."""

    def run(self, identifiers: tuple[str, ...], timeout_seconds: int) -> tuple[TestResult, ...]: ...
