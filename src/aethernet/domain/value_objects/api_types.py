"""Registry-generated AetherNet reference scaffold AET-0041.

Subsystem: Platform & QA. Feature: api. Layer: domain/value_objects.
This is a typed local reference, not a production provider integration.
"""

import re
from dataclasses import dataclass

_IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,127}$")


@dataclass(frozen=True, slots=True)
class ApiIdentifier:
    """Validated, immutable identifier for api."""

    value: str

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.value):
            raise ValueError("invalid resource identifier")

    def __str__(self) -> str:
        return self.value
