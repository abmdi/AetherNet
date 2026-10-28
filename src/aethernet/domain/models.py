"""Provider-independent, immutable cloud inventory models."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class Provider(StrEnum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


@dataclass(frozen=True, slots=True)
class CloudResource:
    provider: Provider
    account_id: str
    resource_id: str
    kind: str
    region: str

    def __post_init__(self) -> None:
        if not all((self.account_id, self.resource_id, self.kind, self.region)):
            raise ValueError("Resource identifiers, kind and region must be non-empty")


@dataclass(frozen=True, slots=True)
class InventorySnapshot:
    snapshot_id: str
    collected_at: datetime
    resources: tuple[CloudResource, ...]

    def __post_init__(self) -> None:
        if not self.snapshot_id:
            raise ValueError("snapshot_id is required")
        if self.collected_at.tzinfo is None or self.collected_at.utcoffset() is None:
            raise ValueError("collected_at must be timezone-aware")

    @classmethod
    def from_resources(cls, snapshot_id: str, resources: tuple[CloudResource, ...]):
        return cls(snapshot_id, datetime.now(UTC), resources)
