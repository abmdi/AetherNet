"""Immutable API route lookup request; never executes state-changing operations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiQuery:
    """Filter registered route metadata using an optional method or scope."""

    method: str | None = None
    required_scope: str | None = None
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.method is not None and self.method not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            raise ValueError("unsupported HTTP method filter")
        if self.required_scope is not None and (
            not self.required_scope or any(c.isspace() for c in self.required_scope)
        ):
            raise ValueError("scope filter must be one identifier")
        if not 1 <= self.limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        if self.offset < 0:
            raise ValueError("offset must be nonnegative")
