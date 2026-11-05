"""Persistence boundary for approved, checksum-pinned schema migrations."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AppliedMigration:
    migration_id: str
    sha256: str
    target_revision: str
    applied_at_utc: str


class MigrationHistoryPort(Protocol):
    """History writes must be transactional and reject checksum drift."""

    def lookup(self, migration_id: str) -> AppliedMigration | None: ...

    def record(self, migration: AppliedMigration) -> None: ...


class MigrationArtifactPort(Protocol):
    """Load an approved migration by immutable artifact identifier."""

    def load(self, migration_id: str) -> bytes: ...
