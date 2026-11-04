"""Evaluate revision-bound CI gates without relying on GitHub or a CI vendor."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class GateStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"


class CiRequest(Protocol):
    revision: str
    required_checks: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    revision: str
    status: GateStatus


@dataclass(frozen=True, slots=True)
class GateEvaluation:
    revision: str
    passed: bool
    failed: tuple[str, ...]
    missing: tuple[str, ...]
    pending: tuple[str, ...]


class CiHandler:
    """Reject missing, stale, pending or failed CI evidence."""

    def evaluate(self, command: CiRequest, results: Mapping[str, CheckResult]) -> GateEvaluation:
        failed: list[str] = []
        missing: list[str] = []
        pending: list[str] = []
        for name in command.required_checks:
            result = results.get(name)
            if result is None or result.revision != command.revision or result.name != name:
                missing.append(name)
            elif result.status is GateStatus.FAILED:
                failed.append(name)
            elif result.status is GateStatus.PENDING:
                pending.append(name)
            elif result.status is not GateStatus.PASSED:
                failed.append(name)
        return GateEvaluation(
            revision=command.revision,
            passed=not (failed or missing or pending) and bool(command.required_checks),
            failed=tuple(failed),
            missing=tuple(missing),
            pending=tuple(pending),
        )
