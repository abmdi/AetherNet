"""Deterministic demo adapter; requires no cloud credentials."""

from aethernet.domain.models import CloudResource, Provider


class DemoCloudAdapter:
    def list_resources(self) -> tuple[CloudResource, ...]:
        return (
            CloudResource(Provider.AWS, "demo-account", "vpc-001", "vpc", "us-east-1"),
            CloudResource(Provider.AWS, "demo-account", "subnet-001", "subnet", "us-east-1"),
        )
