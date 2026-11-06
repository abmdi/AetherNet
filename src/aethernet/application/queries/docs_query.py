"""Validated read-side request for indexed Markdown documentation."""

from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True, slots=True)
class DocsQuery:
    """Bound a documentation listing to a canonical docs/ prefix."""

    prefix: str = "docs/"
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if not self.prefix.startswith("docs/") or "\\" in self.prefix:
            raise ValueError("documentation prefix must start with docs/")
        if any(part in (".", "..") for part in self.prefix.split("/")):
            raise ValueError("documentation prefix must not traverse directories")
        if "//" in self.prefix or len(self.prefix) > 256:
            raise ValueError("documentation prefix must be canonical and bounded")
        if not 1 <= self.limit <= 500 or self.offset < 0:
            raise ValueError("pagination must use limit 1..500 and nonnegative offset")

    def matches(self, path: str) -> bool:
        """Match documents by exact, normalized prefix rather than arbitrary paths."""
        if "\\" in path or ".." in PurePosixPath(path).parts:
            return False
        return path.startswith(self.prefix) and path.endswith(".md")
