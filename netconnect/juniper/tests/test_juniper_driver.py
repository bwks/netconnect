import pytest

from netconnect.juniper.juniper_driver import JuniperDriver


@pytest.fixture()
def setup_juniper_driver():
    dev = JuniperDriver(device='test-dev', username='test-user', password='password')
    return dev


def test_setup_juniper_driver_is_a_juniper_driver_object(setup_juniper_driver):
    assert isinstance(setup_juniper_driver, JuniperDriver)
