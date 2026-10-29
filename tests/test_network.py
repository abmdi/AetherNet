"""Network domain validation tests."""

from dataclasses import FrozenInstanceError

import pytest

from aethernet.domain.models import Provider
from aethernet.domain.network import NetworkResource


def make_resource(**overrides):
    values = {
        "provider": Provider.AWS,
        "account_id": "123456789012",
        "resource_id": "vpc-001",
        "kind": "vpc",
        "region": "us-east-1",
        "cidrs": ("10.20.0.0/16",),
    }
    values.update(overrides)
    return NetworkResource(**values)


def test_valid_network_resource():
    resource = make_resource()
    assert resource.cidrs == ("10.20.0.0/16",)
    assert resource.identity == (
        Provider.AWS,
        "123456789012",
        "vpc-001",
    )


def test_rejects_invalid_cidr():
    with pytest.raises(ValueError):
        make_resource(cidrs=("10.20.0.0/99",))


def test_rejects_noncanonical_cidr():
    with pytest.raises(ValueError):
        make_resource(cidrs=("10.20.1.1/16",))


def test_rejects_public_ip_in_private_field():
    with pytest.raises(ValueError):
        make_resource(private_ips=("8.8.8.8",))


def test_rejects_private_ip_in_public_field():
    with pytest.raises(ValueError):
        make_resource(public_ips=("10.20.1.10",))


def test_accepts_ipv6():
    resource = make_resource(
        cidrs=("2001:db8::/32",),
        private_ips=("fd00::1",),
    )
    assert len(resource.cidrs) == 1


def test_rejects_duplicate_tags():
    with pytest.raises(ValueError):
        make_resource(tags=(("env", "prod"), ("env", "dev")))


def test_resource_is_immutable():
    resource = make_resource()
    with pytest.raises(FrozenInstanceError):
        resource.region = "eu-west-1"


def test_rejects_blank_identity():
    with pytest.raises(ValueError):
        make_resource(resource_id=" ")


def test_rejects_unknown_kind():
    with pytest.raises(ValueError):
        make_resource(kind="unknown")
