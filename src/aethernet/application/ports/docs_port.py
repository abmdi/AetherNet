"""Provider-neutral document storage with explicit immutable hashes."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class DocumentRevision:
    relative_path: str
    sha256: str
    content: str


class DocumentStoragePort(Protocol):
    """Write-once content storage; revisions require an explicit new record."""

    def read(self, relative_path: str) -> DocumentRevision | None: ...

    def put_if_absent(self, revision: DocumentRevision) -> bool: ...


class DocumentIndexPort(Protocol):
    """Provide deterministic metadata discovery independently of storage."""

    def list_paths(self, prefix: str) -> tuple[str, ...]: ...
