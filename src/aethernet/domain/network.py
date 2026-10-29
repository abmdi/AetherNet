"""Provider-independent network resource representations."""

from dataclasses import dataclass, field
from ipaddress import ip_address, ip_network
from typing import Literal

from aethernet.domain.models import Provider

NetworkKind = Literal[
    "vpc",
    "vnet",
    "subnet",
    "network_interface",
    "route_table",
    "security_group",
    "firewall",
    "gateway",
]


@dataclass(frozen=True, slots=True)
class NetworkResource:
    provider: Provider
    account_id: str
    resource_id: str
    kind: NetworkKind
    region: str
    cidrs: tuple[str, ...] = ()
    private_ips: tuple[str, ...] = ()
    public_ips: tuple[str, ...] = ()
    parent_id: str | None = None
    tags: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not all(
            (
                self.account_id.strip(),
                self.resource_id.strip(),
                self.kind,
                self.region.strip(),
            )
        ):
            raise ValueError("Network resource identity fields must be non-empty")

        if self.kind not in NetworkKind.__args__:
            raise ValueError(f"Unsupported network resource kind: {self.kind}")

        if self.parent_id is not None and not self.parent_id.strip():
            raise ValueError("parent_id cannot be blank")

        for cidr in self.cidrs:
            ip_network(cidr, strict=True)

        for address in self.private_ips:
            parsed = ip_address(address)
            if not parsed.is_private:
                raise ValueError(f"Not a private IP address: {address}")

        for address in self.public_ips:
            parsed = ip_address(address)
            if not parsed.is_global:
                raise ValueError(f"Not a globally routable IP address: {address}")

        if len(self.tags) != len({key for key, _ in self.tags}):
            raise ValueError("Duplicate tag keys are not allowed")

    @property
    def identity(self) -> tuple[Provider, str, str]:
        return (self.provider, self.account_id, self.resource_id)
