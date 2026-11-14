"""Registry-generated AetherNet reference scaffold AET-0059.

Subsystem: Platform & QA. Feature: docs. Layer: interfaces/api.
This is a typed local reference, not a production provider integration.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocsRoute:
    """Route descriptor, not a live web server."""

    path: str = "/v1/docs"
    read_method: str = "GET"
    write_method: str = "POST"
    required_scope: str = "docs:write"

    def __post_init__(self) -> None:
        if not self.path.startswith("/") or ".." in self.path:
            raise ValueError("path must be canonical")
        if self.read_method != "GET" or self.write_method != "POST":
            raise ValueError("unsupported method configuration")
        if not self.required_scope:
            raise ValueError("write routes require explicit authorization")
