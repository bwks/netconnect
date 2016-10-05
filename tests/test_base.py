import pytest

from netconnect.base import Connector

@pytest.fixture()
def setup_connector():
    dev = Connector('test-dev')
    return dev


def test_connector_instantiation_is_a_connector_object(setup_connector):
    dev = setup_connector
    assert isinstance(dev, Connector)
