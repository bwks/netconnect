import pytest
import pexpect

from netconnect.juniper.juniper_driver import JuniperDriver


run_tests = False

@pytest.fixture()
def setup_juniper_driver():
    dev = JuniperDriver(device='10.1.1.70', username='lab', password='Password')
    return dev


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_login_with_correct_details_succeeds(setup_juniper_driver):
    setup_juniper_driver.login()


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_login_with_incorrect_password_fails():
    dev = JuniperDriver(device='10.1.1.72', username='lab', password='wrong', timeout=3)
    with pytest.raises(pexpect.TIMEOUT):
        dev.login()


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_login_with_incorrect_username_fails():
    dev = JuniperDriver(device='10.1.1.72', username='wrong', password='Password', timeout=3)
    with pytest.raises(pexpect.TIMEOUT):
        dev.login()


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_get_prompt_returns_correct_prompt(setup_juniper_driver):
    setup_juniper_driver.login()
    assert setup_juniper_driver.get_prompt() == 'lab@lab-vmx-01>'


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_disable_paging_returns_true(setup_juniper_driver):
    setup_juniper_driver.login()
    assert setup_juniper_driver.disable_paging() is True


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_configuration_mode_true(setup_juniper_driver):
    setup_juniper_driver.login()
    assert setup_juniper_driver.disable_paging() is True


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_save_config_returns_true(setup_juniper_driver):
    setup_juniper_driver.login()
    assert setup_juniper_driver.configuration_mode() is True


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_enable_api_with_configuration_mode_returns_true(setup_juniper_driver):
    setup_juniper_driver.login()
    setup_juniper_driver.configuration_mode()
    assert setup_juniper_driver.enable_api() is True


@pytest.mark.skipif(not run_tests, reason='test requires juniper device')
def test_enable_api_without_configuration_mode_returns_true(setup_juniper_driver):
    setup_juniper_driver.login()
    assert setup_juniper_driver.enable_api() is True
