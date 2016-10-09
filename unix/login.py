import pexpect
import logging

from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)


# Settings
logging.basicConfig(level=logging.DEBUG)


class UnixLogin(BaseLogin):
    def login(self, login_type='ssh'):
        """
        Login to linux/unix shell (bash terminal assumed)
        :param login_type: SSH or Telnet
        :return: pexpect spawn object

        Authentication types:
         - username and password
         - certificate based
        """
        validate_login_type(login_type)

        login_cmd = self.ssh_driver if login_type.lower() == 'ssh' else self.telnet_driver

        child = pexpect.spawn(login_cmd)
        i = child.expect(PEXPECT_ERRORS + ['[#\$]', '.*assword.*'])
        if i == (0 or 1):
            clean_up_error(child, i)
        elif i == 2:
            logging.debug('logged in to bash')
            return child
        elif i == 3:
            child.sendline(self.password)
            j = child.expect(PEXPECT_ERRORS + ['[#\$]'])
            if j == (0 or 1):
                clean_up_error(child, j)
            elif j == 2:
                logging.debug('logged in to bash')
                return child
