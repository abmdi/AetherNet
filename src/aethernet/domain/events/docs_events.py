"""Registry-generated AetherNet reference scaffold AET-0034.

Subsystem: Platform & QA. Feature: docs. Layer: domain/events.
This is a typed local reference, not a production provider integration.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DocsEvent:
    """Immutable event evidence for a docs resource."""

    event_id: str
    resource_id: str
    occurred_at: datetime
    kind: str

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.resource_id.strip():
            raise ValueError("event and resource identifiers are required")
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware")
        if self.kind not in ("created", "updated", "deleted", "observed"):
            raise ValueError("unsupported event kind")
