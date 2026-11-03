"""Publication request for a bounded Markdown documentation artifact."""

import re
from dataclasses import dataclass

_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class DocsCommand:
    """Validate document input while leaving persistence to an application handler."""

    slug: str
    title: str
    markdown: str

    def __post_init__(self) -> None:
        if not _SLUG.fullmatch(self.slug) or len(self.slug) > 96:
            raise ValueError("slug must be a short canonical URL identifier")
        if not self.title.strip() or len(self.title) > 200:
            raise ValueError("title must be between 1 and 200 characters")
        if not self.markdown.strip() or len(self.markdown.encode("utf-8")) > 1_000_000:
            raise ValueError("markdown must be nonempty and at most 1 MB")

    @property
    def relative_path(self) -> str:
        return f"docs/{self.slug}.md"
