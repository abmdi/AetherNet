"""Immutable, bounded request describing a deterministic Python test selection."""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath


class TestScope(StrEnum):
    UNIT = "unit"
    INTEGRATION = "integration"
    SCENARIO = "scenario"


@dataclass(frozen=True, slots=True)
class UnitTestsCommand:
    """Describe tests to select, never execute arbitrary shell commands."""

    scope: TestScope
    identifiers: tuple[str, ...] = ()
    timeout_seconds: int = 120
    fail_fast: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.scope, TestScope):
            raise TypeError("scope must be a TestScope")
        if not isinstance(self.timeout_seconds, int) or not 1 <= self.timeout_seconds <= 3600:
            raise ValueError("timeout_seconds must be within 1..3600")
        if len(self.identifiers) > 256 or len(set(self.identifiers)) != len(self.identifiers):
            raise ValueError("identifiers must be unique and at most 256")
        for identifier in self.identifiers:
            path = PurePosixPath(identifier)
            if (
                not identifier
                or identifier.startswith(("/", "-"))
                or "\\" in identifier
                or any(ch.isspace() for ch in identifier)
                or any(part in ("", ".", "..") for part in identifier.split("/"))
                or path.suffix not in ("", ".py")
            ):
                raise ValueError("test identifiers must be safe relative paths")
