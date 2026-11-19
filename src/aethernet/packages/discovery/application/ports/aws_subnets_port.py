"""Registry-generated AetherNet reference scaffold AET-0079.

Subsystem: Discovery. Feature: aws_subnets. Layer: application/ports.
This is a typed local reference, not a production provider integration.
"""

from collections.abc import Mapping
from typing import Protocol


class AwsSubnetsPort(Protocol):
    """Injected provider-neutral boundary for aws_subnets."""

    def fetch(self, resource_id: str) -> Mapping[str, object] | None: ...

    def store(self, resource_id: str, record: Mapping[str, object]) -> None: ...

    def remove(self, resource_id: str) -> bool: ...
