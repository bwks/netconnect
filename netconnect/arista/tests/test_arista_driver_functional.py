import pytest
import pexpect

from netconnect.arista.arista_driver import AristaDriver


run_tests = False

@pytest.fixture()
def setup_arista_driver():
    dev = AristaDriver(device='10.1.1.72', username='lab', password='Password')
    return dev


@pytest.mark.skipif(not run_tests, reason='test requires arista device')
def test_enable_api_returns_true(setup_arista_driver):
    setup_arista_driver.login(enable_password='Password')
    assert setup_arista_driver.enable_api() is True
