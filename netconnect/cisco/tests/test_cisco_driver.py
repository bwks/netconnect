import pytest
from unittest.mock import patch, Mock

from netconnect.cisco.cisco_driver import CiscoDriver


@pytest.fixture()
def setup_cisco_driver():
    dev = CiscoDriver(device='test-dev', username='test-user', password='password')
    return dev


@patch.object(CiscoDriver, 'disable_paging')
def fake_disable_paging(mock_disable_paging):
    mock_disable_paging.return_value = True
    return CiscoDriver.disable_paging()


def test_setup_cisco_driver_is_a_cisco_driver_object(setup_cisco_driver):
    assert isinstance(setup_cisco_driver, CiscoDriver)


def test_disable_paging_returns_true():
    assert fake_disable_paging() is True
