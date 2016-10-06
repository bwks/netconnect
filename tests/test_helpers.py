import pytest

from netconnect.helpers import parse_error
from pexpect.exceptions import EOF, TIMEOUT


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


def test_parse_error_timout_message():
    with pytest.raises(TIMEOUT) as e:
        parse_error(1)
        assert e.value.message == 'Got Timeout'
