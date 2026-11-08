"""Registry-generated AetherNet reference scaffold AET-0026.

Subsystem: Platform & QA. Feature: api. Layer: domain/entities.
This is a typed local reference, not a production provider integration.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ApiModel:
    """Stable identity and immutable attributes for api."""

    resource_id: str
    revision: int = 0
    attributes: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.resource_id or self.resource_id.strip() != self.resource_id:
            raise ValueError("resource_id is required")
        if self.revision < 0:
            raise ValueError("revision must be nonnegative")
        if len({key for key, _ in self.attributes}) != len(self.attributes):
            raise ValueError("duplicate attribute key")
