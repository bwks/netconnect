import pytest

from netconnect.cisco.cisco_asa_driver import CiscoASADriver

# Test Variables
run_tests = False
test_device = '10.1.1.79'
test_user = 'lab'
test_pass = 'Password'
test_enable_pass = 'Password'

@pytest.fixture()
def setup_asa_cisco_driver():
    dev = CiscoASADriver(device=test_device, username=test_user, password=test_pass)
    return dev


@pytest.mark.skipif(not run_tests, reason='test requires cisco asa device')
def test_get_prompt_returns_correct_prompt(setup_asa_cisco_driver):
    setup_asa_cisco_driver.login(enable_password=test_enable_pass)
    assert setup_asa_cisco_driver.get_prompt() == 'lab-asa-01#'


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_disable_paging_returns_true(setup_asa_cisco_driver):
    setup_asa_cisco_driver.login(enable_password=test_enable_pass)
    assert setup_asa_cisco_driver.disable_paging() is True