"""Provider-neutral CI status and immutable revision boundaries."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class JobState(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class JobObservation:
    revision: str
    name: str
    state: JobState
    observation_id: str


class CiStatusPort(Protocol):
    """Return observations pinned to the requested source revision."""

    def checks_for(self, revision: str) -> tuple[JobObservation, ...]: ...


class RevisionResolverPort(Protocol):
    """Resolve an immutable commit from a mutable branch reference."""

    def commit_for(self, ref: str) -> str: ...
