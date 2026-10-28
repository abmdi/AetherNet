"""Minimal HTTP entrypoint, with no SDK dependencies in the domain."""

from fastapi import FastAPI

from aethernet.adapters.demo import DemoCloudAdapter
from aethernet.application.discovery import DiscoveryService

app = FastAPI(title="AetherNet", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/demo/inventory")
def demo_inventory() -> dict[str, object]:
    snapshot = DiscoveryService(DemoCloudAdapter()).collect("demo-snapshot")
    return {
        "snapshot_id": snapshot.snapshot_id,
        "collected_at": snapshot.collected_at.isoformat(),
        "resources": [
            {
                "provider": r.provider.value,
                "account_id": r.account_id,
                "resource_id": r.resource_id,
                "kind": r.kind,
                "region": r.region,
            }
            for r in snapshot.resources
        ],
    }
