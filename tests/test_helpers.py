import pytest
import sys

from netconnect.helpers import parse_error, validate_login_type, get_prompt, send_commands
from pexpect.exceptions import EOF, TIMEOUT

if sys.version_info >= (3, 3):
    from unittest.mock import Mock, patch
else:
    from mock import Mock, patch


def setup_fake_child(fake_string):
    fake_child = Mock()
    fake_child.send_control.return_value = ''
    fake_child.expect.return_value = 'lab-gw-01#'
    fake_child.after.decode.return_value = '{0}lab-gw-01#'.format(fake_string)
    fake_child.sendline.return_value = ''
    fake_child.before.decode.return_value = 'show version output'
    return fake_child


def test_get_prompt_returns_correct_prompt():
    split_list = ['\x1b[5n', '\r\n\r\n', '\r\n\r', '\r\n', '\n']
    for split in split_list:
        assert 'lab-gw-01#' == get_prompt(setup_fake_child(split))


def test_send_commands_returns_list():
    assert isinstance(send_commands(setup_fake_child(''), 'lab-gw-01#', 'show version'), list)


def test_send_commands_with_commands_not_set_raises_value_error():
    with pytest.raises(ValueError):
        send_commands(setup_fake_child(''), 'lab-gw-01#')


def test_parse_error_raises_eof():
    with pytest.raises(EOF):
        parse_error(0)


def test_parse_error_eof_message():
    with pytest.raises(EOF) as e:
        parse_error(0)
        assert e.value.message == 'Got EOF'


def test_parse_error_raises_timeout():
    with pytest.raises(TIMEOUT):
        parse_error(1)


def test_parse_error_timeout_message():
    with pytest.raises(TIMEOUT) as e:
        parse_error(1)
        assert e.value.message == 'Got Timeout'


def test_validate_login_type_raises_value_error():
    with pytest.raises(ValueError):
        validate_login_type('invalid')


def test_validate_login_type_with_telnet_does_not_raise_value_error():
    assert validate_login_type('telnet') is True


def test_validate_login_type_with_ssh_does_not_raise_value_error():
    assert validate_login_type('ssh') is True


