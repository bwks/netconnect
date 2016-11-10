import pytest

from netconnect.cisco.cisco_driver import CiscoDriver


@pytest.fixture()
def setup_cisco_driver():
    dev = CiscoDriver(device='test-dev', username='test-user', password='password')
    return dev


def test_setup_cisco_driver_is_a_cisco_driver_object(setup_cisco_driver):
    assert isinstance(setup_cisco_driver, CiscoDriver)
