import pytest

from netconnect.arista.arista_driver import AristaDriver


# Test Variables
run_tests = False
test_device = '10.1.1.72'
test_user = 'lab'
test_pass = 'Password'
test_enable_pass = 'Password'


@pytest.fixture()
def setup_arista_driver():
    dev = AristaDriver(device=test_device, username=test_user, password=test_pass)
    return dev


@pytest.mark.skipif(not run_tests, reason='test requires arista device')
def test_enable_api_returns_true(setup_arista_driver):
    setup_arista_driver.login(enable_password=test_enable_pass)
    assert setup_arista_driver.enable_api() is True
