"""Validated, immutable read-side request for CI observations.

Queries select immutable revision evidence; they neither trigger jobs nor
change CI gate outcomes.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CiQuery:
    """Select check observations for one revision with bounded pagination."""

    revision: str
    check_names: tuple[str, ...] = ()
    include_pending: bool = True
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if not self.revision or self.revision.strip() != self.revision:
            raise ValueError("revision must be a nonempty trimmed reference")
        if len(self.revision) > 128 or any(char.isspace() for char in self.revision):
            raise ValueError("revision must not contain whitespace or exceed 128 characters")
        if len(self.check_names) > 256 or len(set(self.check_names)) != len(self.check_names):
            raise ValueError("check names must be unique and at most 256")
        if any(not name or name.strip() != name for name in self.check_names):
            raise ValueError("check names must be nonempty and trimmed")
        if not 1 <= self.limit <= 500 or self.offset < 0:
            raise ValueError("pagination must use limit 1..500 and nonnegative offset")

    def selects(self, check_name: str, status: str) -> bool:
        """Return whether a CI observation is in the requested result set."""
        if self.check_names and check_name not in self.check_names:
            return False
        return self.include_pending or status != "pending"
