import pytest

from netconnect.arista.arista_driver import AristaDriver


@pytest.fixture()
def setup_arista_driver():
    dev = AristaDriver(device='test-dev', username='test-user', password='password')
    return dev


def test_setup_arista_driver_is_a_arista_driver_object(setup_arista_driver):
    assert isinstance(setup_arista_driver, AristaDriver)
