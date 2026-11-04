"""Checksum-pinned migration planning; deliberately never executes SQL."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol


class MigrationRequest(Protocol):
    migration_id: str
    sha256: str
    target_revision: str

    def matches_artifact(self, content: bytes) -> bool: ...


@dataclass(frozen=True, slots=True)
class MigrationDecision:
    migration_id: str
    target_revision: str
    action: str


class DatabaseHandler:
    """Produce a safe decision from trusted migration history and artifact bytes."""

    def plan(
        self,
        command: MigrationRequest,
        artifact: bytes,
        applied_checksums: Mapping[str, str],
    ) -> MigrationDecision:
        if not artifact or not command.matches_artifact(artifact):
            raise ValueError("migration checksum mismatch")
        applied = applied_checksums.get(command.migration_id)
        if applied is not None and applied != command.sha256:
            raise ValueError("already applied migration has different checksum")
        action = "already_applied" if applied == command.sha256 else "requires_approval"
        return MigrationDecision(command.migration_id, command.target_revision, action)
