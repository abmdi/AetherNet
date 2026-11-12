"""Registry-generated AetherNet reference scaffold AET-0049.

Subsystem: Platform & QA. Feature: docs. Layer: infrastructure/adapters.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Callable, Mapping


class DocsAdapter:
    """Inject a transport; no live provider credentials are embedded."""

    def __init__(
        self,
        transport: Callable[[str, Mapping[str, str]], Mapping[str, str]],
    ) -> None:
        self._transport = transport

    def fetch(self, resource_id: str) -> dict[str, str]:
        if not resource_id.strip():
            raise ValueError("resource_id is required")
        result = self._transport(resource_id, {"feature": "docs"})
        return dict(result)
