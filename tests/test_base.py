import pytest

from netconnect.base import Connector

@pytest.fixture()
def setup_connector():
    dev = Connector(device='test-dev')
    return dev


def test_connector_instantiation_is_a_connector_object(setup_connector):
    assert isinstance(setup_connector, Connector)


def test_telnet_driver_syntax():
    dev = Connector(device='test-dev', port=23)
    assert dev.telnet_driver == 'telnet test-dev 23'


def test_conenctor_with_ssh_config_file_and_ignore_ssh_config_raises_attribute_error():
    with pytest.raises(AttributeError):
        Connector(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=True)


def test_conenctor_with_ssh_config_file_and_ignore_ssh_config_attribute_error_message():
    with pytest.raises(AttributeError) as e:
        Connector(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=True)
        assert e.value.message == ('cannot define ssh_config_file '
                                   'and set ignore_ssh_config to True')


def test_connector_with_defaults_matches_ssh_driver_syntax(setup_connector):
    ssh_cmd = ('ssh -p 22 -o UserKnownHostsFile=/dev/null '
               '-o StrictHostKeyChecking=no -F /dev/null test-dev')
    assert setup_connector.ssh_driver == ssh_cmd


def test_connector_options_ssh_config_file_and_ignore_ssh_config_ssh_driver_syntax():
    dev = Connector(device='test-dev', ssh_config_file='~/.ssh/config', ignore_ssh_config=False)
    assert dev.ssh_driver == ('ssh -p 22 -o UserKnownHostsFile=/dev/null '
                              '-o StrictHostKeyChecking=no -F ~/.ssh/config test-dev')

