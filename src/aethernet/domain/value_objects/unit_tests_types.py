"""Registry-generated AetherNet reference scaffold AET-0045.

Subsystem: Platform & QA. Feature: unit_tests. Layer: domain/value_objects.
This is a typed local reference, not a production provider integration.
"""

import re
from dataclasses import dataclass

_IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,127}$")


@dataclass(frozen=True, slots=True)
class UnitTestsIdentifier:
    """Validated, immutable identifier for unit_tests."""

    value: str

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.value):
            raise ValueError("invalid resource identifier")

    def __str__(self) -> str:
        return self.value
