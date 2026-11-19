"""Registry-generated AetherNet reference scaffold AET-0081.

Subsystem: Discovery. Feature: azure_nsg. Layer: application/ports.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Mapping
from typing import Protocol


class AzureNsgPort(Protocol):
    """Injected provider-neutral boundary for azure_nsg."""

    def fetch(self, resource_id: str) -> Mapping[str, object] | None: ...

    def store(self, resource_id: str, record: Mapping[str, object]) -> None: ...

    def remove(self, resource_id: str) -> bool: ...
