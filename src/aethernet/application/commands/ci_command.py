"""Validated request to apply an explicit CI quality gate."""

from dataclasses import dataclass
from enum import StrEnum


class CheckStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"


@dataclass(frozen=True, slots=True)
class CiCommand:
    """Evaluate required named checks; missing or pending checks never pass."""

    revision: str
    required_checks: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.revision or not self.revision.strip():
            raise ValueError("revision is required")
        if not self.required_checks or len(set(self.required_checks)) != len(self.required_checks):
            raise ValueError("required checks must be nonempty and unique")
        if any(not check or not check.strip() for check in self.required_checks):
            raise ValueError("check names must be nonempty")

    def passes(self, observed: dict[str, CheckStatus]) -> bool:
        return all(observed.get(name) is CheckStatus.PASSED for name in self.required_checks)
