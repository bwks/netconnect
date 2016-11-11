import pytest

from netconnect.unix.unix_driver import UnixDriver


@pytest.fixture()
def setup_unix_driver():
    dev = UnixDriver(device='test-dev', username='test-user', password='password')
    return dev


def test_setup_unix_driver_is_a_unix_driver_object(setup_unix_driver):
    assert isinstance(setup_unix_driver, UnixDriver)
