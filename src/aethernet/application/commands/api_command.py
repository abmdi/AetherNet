"""Immutable API route registration request with explicit authorization metadata."""

from dataclasses import dataclass
from enum import StrEnum


class HttpMethod(StrEnum):
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass(frozen=True, slots=True)
class ApiCommand:
    """Describe a state-changing route without performing any network I/O."""

    method: HttpMethod
    path: str
    operation_id: str
    required_scope: str

    def __post_init__(self) -> None:
        if not isinstance(self.method, HttpMethod):
            raise TypeError("method must be a supported state-changing HttpMethod")
        if not self.path.startswith("/") or "//" in self.path or ".." in self.path:
            raise ValueError("path must be an absolute, canonical API path")
        for name, value in (
            ("operation_id", self.operation_id),
            ("required_scope", self.required_scope),
        ):
            if not value or not value.strip() or any(char.isspace() for char in value):
                raise ValueError(f"{name} must be a nonempty identifier without whitespace")

    @property
    def route_key(self) -> str:
        return f"{self.method.value} {self.path}"
