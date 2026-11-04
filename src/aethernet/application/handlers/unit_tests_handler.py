"""Deterministic test selection, independent of pytest invocation or shell execution."""

from dataclasses import dataclass
from typing import Protocol


class TestRequest(Protocol):
    scope: object
    identifiers: tuple[str, ...]
    timeout_seconds: int
    fail_fast: bool


@dataclass(frozen=True, slots=True)
class TestPlan:
    selected: tuple[str, ...]
    timeout_seconds: int
    fail_fast: bool


class UnitTestsHandler:
    """Restrict selection to an explicitly enumerated trusted test inventory."""

    def select(self, command: TestRequest, inventory: tuple[str, ...]) -> TestPlan:
        scope = str(getattr(command.scope, "value", command.scope))
        if scope not in ("unit", "integration", "scenario"):
            raise ValueError("unsupported test scope")
        base = f"tests/{scope}/"
        scoped = tuple(sorted({path for path in inventory if path.startswith(base)}))
        if not scoped:
            raise LookupError(f"no tests registered for scope {scope}")
        if command.identifiers:
            requested = set(command.identifiers)
            selected = tuple(path for path in scoped if path in requested)
            if len(selected) != len(requested):
                raise ValueError("requested tests are not in the trusted inventory and scope")
        else:
            selected = scoped
        return TestPlan(selected, command.timeout_seconds, command.fail_fast)
