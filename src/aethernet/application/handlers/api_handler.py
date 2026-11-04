"""In-memory registration of state-changing HTTP route contracts.

No transport is opened; frameworks can project these contracts into routers.
"""

from dataclasses import dataclass
from typing import Protocol


class RouteCommand(Protocol):
    @property
    def route_key(self) -> str: ...

    @property
    def operation_id(self) -> str: ...

    @property
    def required_scope(self) -> str: ...


@dataclass(frozen=True, slots=True)
class RouteDescriptor:
    key: str
    operation_id: str
    required_scope: str


class ApiHandler:
    """Keep an auditable, collision-free registry of write operations."""

    def __init__(self) -> None:
        self._routes: dict[str, RouteDescriptor] = {}
        self._operation_ids: dict[str, str] = {}

    def register(self, command: RouteCommand) -> RouteDescriptor:
        route = RouteDescriptor(command.route_key, command.operation_id, command.required_scope)
        if not all((route.key, route.operation_id, route.required_scope)):
            raise ValueError("route metadata must be populated")
        existing = self._routes.get(route.key)
        if existing is not None:
            if existing == route:
                return existing
            raise ValueError(f"route collision: {route.key}")
        if route.operation_id in self._operation_ids:
            raise ValueError(f"duplicate operation ID: {route.operation_id}")
        self._routes[route.key] = route
        self._operation_ids[route.operation_id] = route.key
        return route

    def authorize(self, route_key: str, granted_scopes: frozenset[str]) -> RouteDescriptor:
        route = self._routes.get(route_key)
        if route is None:
            raise LookupError("unknown route")
        if route.required_scope not in granted_scopes:
            raise PermissionError(f"scope required: {route.required_scope}")
        return route

    def snapshot(self) -> tuple[RouteDescriptor, ...]:
        return tuple(sorted(self._routes.values(), key=lambda value: value.key))
