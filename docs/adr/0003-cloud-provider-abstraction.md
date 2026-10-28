# ADR-003: Cloud Provider Abstraction

Status: Proposed — 2026-10-28

## Decision
The domain stores normalized immutable resource records independent of cloud SDKs.
Provider-specific adapters implement an application-layer `DiscoveryPort` protocol.
Discovery snapshots are timezone-aware and contain a consistent tuple of resources.

## Consequences
- Unit tests run without real cloud credentials.
- SDK credentials stay in adapters and are never serialized into snapshots.
- AWS/Azure/GCP connectors can be implemented incrementally.
- A future production snapshot repository will enforce durable IDs and versioning.

## Validation
The demo adapter and HTTP endpoint exercise the discovery use case without SDK imports.
