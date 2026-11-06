"""Immutable request for inspecting previously applied schema migrations."""

import re
from dataclasses import dataclass

_MIGRATION_ID = re.compile(r"^[a-z][a-z0-9_]{2,79}$")


@dataclass(frozen=True, slots=True)
class DatabaseQuery:
    """Read-only filter; never executes or approves a schema migration."""

    migration_id: str | None = None
    revision: str | None = None
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.migration_id is not None and not _MIGRATION_ID.fullmatch(self.migration_id):
            raise ValueError("migration_id must be canonical snake_case")
        if self.revision is not None and (
            not self.revision.strip()
            or self.revision != self.revision.strip()
            or len(self.revision) > 128
        ):
            raise ValueError("revision must be a nonempty trimmed reference")
        if not 1 <= self.limit <= 500 or self.offset < 0:
            raise ValueError("pagination must use limit 1..500 and nonnegative offset")

    def matches(self, migration_id: str, revision: str) -> bool:
        """Match a migration record without retrieving or modifying its payload."""
        return (self.migration_id is None or migration_id == self.migration_id) and (
            self.revision is None or revision == self.revision
        )
