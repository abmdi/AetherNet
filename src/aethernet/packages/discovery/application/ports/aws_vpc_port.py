"""Registry-generated AetherNet reference scaffold AET-0080.

Subsystem: Discovery. Feature: aws_vpc. Layer: application/ports.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Mapping
from typing import Protocol


class AwsVpcPort(Protocol):
    """Injected provider-neutral boundary for aws_vpc."""

    def fetch(self, resource_id: str) -> Mapping[str, object] | None: ...

    def store(self, resource_id: str, record: Mapping[str, object]) -> None: ...

    def remove(self, resource_id: str) -> bool: ...
