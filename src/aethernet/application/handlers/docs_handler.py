"""Conflict-aware documentation staging in memory, with no filesystem access."""

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol


class DocumentRequest(Protocol):
    slug: str
    title: str
    markdown: str

    @property
    def relative_path(self) -> str: ...


@dataclass(frozen=True, slots=True)
class DocumentArtifact:
    path: str
    title: str
    body: str
    sha256: str


class DocsHandler:
    """Prepare canonical Markdown documents without overwriting different content."""

    def prepare(
        self,
        command: DocumentRequest,
        existing: Mapping[str, str],
    ) -> DocumentArtifact:
        path = command.relative_path
        if not path.startswith("docs/") or not path.endswith(".md"):
            raise ValueError("invalid document destination")
        body = f"# {command.title.strip()}\n\n{command.markdown.strip()}\n"
        previous = existing.get(path)
        if previous is not None and previous != body:
            raise ValueError(f"conflicting document: {path}")
        return DocumentArtifact(
            path, command.title.strip(), body, sha256(body.encode()).hexdigest()
        )
