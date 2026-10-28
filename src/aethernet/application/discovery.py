"""Cloud discovery use case with an injected provider adapter."""

from typing import Protocol

from aethernet.domain.models import CloudResource, InventorySnapshot


class DiscoveryPort(Protocol):
    def list_resources(self) -> tuple[CloudResource, ...]: ...


class DiscoveryService:
    def __init__(self, provider: DiscoveryPort) -> None:
        self._provider = provider

    def collect(self, snapshot_id: str) -> InventorySnapshot:
        resources = self._provider.list_resources()
        ids = [(r.provider, r.account_id, r.resource_id) for r in resources]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate resource identifiers in discovery result")
        return InventorySnapshot.from_resources(snapshot_id, resources)
