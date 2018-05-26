import pytest

from netconnect.base import BaseDriver


@pytest.fixture()
def setup_base_login():
    dev = BaseDriver(device='test-dev')
    return dev


@pytest.fixture()
def setup_ssh_no_defaults():
    dev = BaseDriver(
        device='test-dev', username='test-user', password='password',
        ignore_ssh_config=False, ignore_known_hosts=False, disable_host_key_checking=True)
    return dev


def test_base_login_password(setup_ssh_no_defaults):
    assert setup_ssh_no_defaults.password == 'password'


def test_base_login_timeout(setup_ssh_no_defaults):
    assert setup_ssh_no_defaults.timeout == 5


def test_base_login_device(setup_ssh_no_defaults):
    assert setup_ssh_no_defaults.device == 'test-dev'


def test_base_login_ssh_port(setup_ssh_no_defaults):
    assert setup_ssh_no_defaults.ssh_port == 22


def test_base_login_disable_host_key_checking(setup_ssh_no_defaults):
    assert setup_ssh_no_defaults.disable_host_key_checking is True


def test_base_login_options_with_ssh_key_file_ssh_driver_syntax():
    dev = BaseDriver(
        device='test-dev', ssh_key_file='~/.ssh/config',
        ignore_ssh_config=False, ignore_known_hosts=False, disable_host_key_checking=True)
    expected = 'ssh -p 22 -o StrictHostKeyChecking=no -o IdentityFile=~/.ssh/config test-dev'
    assert dev.ssh_driver == expected


def test_base_login_with_no_port_ssh_driver_syntax():
    dev = BaseDriver(
        device='test-dev', username='test-user', password='password',
        ignore_ssh_config=False, ignore_known_hosts=False, disable_host_key_checking=True)
    assert dev.ssh_driver == 'ssh -p 22 -l test-user -o StrictHostKeyChecking=no test-dev'


def test_base_login_instantiation_is_a_connector_object(setup_base_login):
    assert isinstance(setup_base_login, BaseDriver)


def test_base_login_options_username_password_ssh_driver_syntax(setup_ssh_no_defaults):
    expected = 'ssh -p 22 -l test-user -o StrictHostKeyChecking=no test-dev'
    assert setup_ssh_no_defaults.ssh_driver == expected


def test_telnet_driver_syntax():
    dev = BaseDriver(device='test-dev', telnet_port=23)
    assert dev.telnet_driver == 'telnet test-dev 23'


def test_base_login_with_ssh_config_file_and_ignore_ssh_config_raises_attribute_error():
    with pytest.raises(AttributeError):
        BaseDriver(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=True)


def test_base_login_with_ssh_config_file_and_ignore_ssh_config_attribute_error_message():
    with pytest.raises(AttributeError) as e:
        BaseDriver(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=True)
        assert e.value.message == ('cannot define ssh_config_file '
                                   'and set ignore_ssh_config to True')


def test_base_login_with_defaults_matches_ssh_driver_syntax(setup_base_login):
    ssh_cmd = 'ssh -p 22 -o UserKnownHostsFile=/dev/null -F /dev/null test-dev'
    assert setup_base_login.ssh_driver == ssh_cmd


def test_base_login_options_ssh_config_file_and_ignore_ssh_config_ssh_driver_syntax():
    dev = BaseDriver(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=False)
    assert dev.ssh_driver == 'ssh -p 22 -o UserKnownHostsFile=/dev/null -F ~/.ssh/config test-dev'
