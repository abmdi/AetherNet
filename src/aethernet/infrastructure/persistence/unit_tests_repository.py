"""Registry-generated AetherNet reference scaffold AET-0055.

Subsystem: Platform & QA. Feature: unit_tests. Layer: infrastructure/persistence.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Mapping


class UnitTestsRepository:
    """In-memory reference storage; production persistence is not provided."""

    def __init__(self) -> None:
        self._rows: dict[str, dict[str, str]] = {}

    def put(self, resource_id: str, value: Mapping[str, str]) -> None:
        if not resource_id.strip():
            raise ValueError("resource_id is required")
        self._rows[resource_id] = dict(value)

    def get(self, resource_id: str) -> dict[str, str] | None:
        item = self._rows.get(resource_id)
        return dict(item) if item is not None else None

    def remove(self, resource_id: str) -> bool:
        return self._rows.pop(resource_id, None) is not None
