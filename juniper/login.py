import pexpect
import logging

from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)


class JuniperLogin(BaseLogin):
    def login(self):
        pass
