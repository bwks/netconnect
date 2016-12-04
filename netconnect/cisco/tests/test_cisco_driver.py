import sys
import pytest

if sys.version_info >= (3, 3):
    from unittest.mock import Mock, patch
else:
    from mock import Mock, patch

from netconnect.cisco.cisco_driver import CiscoDriver
from netconnect.exceptions import (
    LoginTimeoutError,
)


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


def test_login_to_invalid_device_raises_login_timeout_error():
    dev = CiscoDriver(device='no_device', username='test-user', password='password', timeout=1)
    with pytest.raises(LoginTimeoutError):
        dev.login()
