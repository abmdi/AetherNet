"""Safe metadata-only migration request; never executes arbitrary SQL."""

import re
from dataclasses import dataclass

_MIGRATION_ID = re.compile(r"^[a-z][a-z0-9_]{2,79}$")
_CHECKSUM = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True, slots=True)
class DatabaseCommand:
    """Pin an approved migration artifact to a predictable checksum."""

    migration_id: str
    sha256: str
    target_revision: str

    def __post_init__(self) -> None:
        if not _MIGRATION_ID.fullmatch(self.migration_id):
            raise ValueError("migration_id must be lowercase snake_case")
        if not _CHECKSUM.fullmatch(self.sha256):
            raise ValueError("sha256 must contain 64 lowercase hexadecimal characters")
        if not self.target_revision or not self.target_revision.strip():
            raise ValueError("target_revision is required")

    def matches_artifact(self, content: bytes) -> bool:
        from hashlib import sha256

        return sha256(content).hexdigest() == self.sha256
