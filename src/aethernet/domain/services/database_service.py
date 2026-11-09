"""Registry-generated AetherNet reference scaffold AET-0038.

Subsystem: Platform & QA. Feature: database. Layer: domain/services.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Iterable, Mapping


class DatabaseService:
    """Pure, deterministic operations on database domain records."""

    @staticmethod
    def merge(previous: Mapping[str, str], incoming: Mapping[str, str]) -> dict[str, str]:
        merged = dict(previous)
        for key, value in incoming.items():
            if not key or not isinstance(value, str):
                raise ValueError("invalid domain attribute")
            merged[key] = value
        return merged

    @staticmethod
    def stable_ids(records: Iterable[str]) -> tuple[str, ...]:
        if any(not record for record in records):
            raise ValueError("empty resource identifier")
        return tuple(sorted(set(records)))
