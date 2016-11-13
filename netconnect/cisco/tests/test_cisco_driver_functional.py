import pytest
import pexpect

from netconnect.cisco.cisco_driver import CiscoDriver


run_tests = True

@pytest.fixture()
def setup_cisco_driver():
    dev = CiscoDriver(device='10.1.1.71', username='lab', password='Password')
    return dev


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_login_with_correct_details_succeeds(setup_cisco_driver):
    setup_cisco_driver.login(enable_password='Password')


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_login_with_incorrect_password_fails():
    dev = CiscoDriver(device='10.1.1.71', username='lab', password='wrong', timeout=3)
    with pytest.raises(pexpect.TIMEOUT):
        dev.login()


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_login_with_incorrect_username_fails():
    dev = CiscoDriver(device='10.1.1.71', username='wrong', password='Password', timeout=3)
    with pytest.raises(pexpect.TIMEOUT):
        dev.login()


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_login_with_correct_details_and_no_enable_password_raises_value_error(setup_cisco_driver):
    with pytest.raises(ValueError):
        setup_cisco_driver.login()


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_get_prompt_returns_correct_prompt(setup_cisco_driver):
    setup_cisco_driver.login(enable_password='Password')
    assert setup_cisco_driver.get_prompt() == 'lab-csr-01#'


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_disable_paging_returns_true(setup_cisco_driver):
    setup_cisco_driver.login(enable_password='Password')
    assert setup_cisco_driver.disable_paging() is True


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_save_config_returns_true(setup_cisco_driver):
    setup_cisco_driver.login(enable_password='Password')
    assert setup_cisco_driver.save_config() is True


@pytest.mark.skipif(not run_tests, reason='test requires cisco device')
def test_configuration_mode_returns_true(setup_cisco_driver):
    setup_cisco_driver.login(enable_password='Password')
    assert setup_cisco_driver.configuration_mode() is True

