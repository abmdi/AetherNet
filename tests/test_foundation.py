from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from aethernet.adapters.demo import DemoCloudAdapter
from aethernet.api import app
from aethernet.application.discovery import DiscoveryService
from aethernet.domain.models import CloudResource, InventorySnapshot, Provider


def test_demo_discovery():
    snapshot = DiscoveryService(DemoCloudAdapter()).collect("snap-1")
    assert len(snapshot.resources) == 2
    assert snapshot.resources[0].provider == Provider.AWS


def test_rejects_naive_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        InventorySnapshot("snap-1", datetime(2026, 11, 3), ())


def test_accepts_aware_timestamp():
    snapshot = InventorySnapshot("snap-1", datetime.now(UTC), ())
    assert snapshot.snapshot_id == "snap-1"


def test_resource_requires_identifiers():
    with pytest.raises(ValueError):
        CloudResource(Provider.AWS, "", "vpc-1", "vpc", "us-east-1")


def test_http_endpoints():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    response = client.get("/demo/inventory")
    assert response.status_code == 200
    assert len(response.json()["resources"]) == 2
