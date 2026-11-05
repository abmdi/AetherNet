"""Framework-independent route discovery and authorization boundaries."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RouteRecord:
    method: str
    path: str
    operation_id: str
    required_scope: str


class RouteCatalogPort(Protocol):
    """Implementations must reject duplicate route keys and operation IDs."""

    def register(self, record: RouteRecord) -> None: ...

    def get(self, method: str, path: str) -> RouteRecord | None: ...

    def list_routes(self) -> tuple[RouteRecord, ...]: ...


class ScopeAuthorizerPort(Protocol):
    """Authorization decisions are separate from transport details."""

    def permits(self, principal_id: str, required_scope: str) -> bool: ...
