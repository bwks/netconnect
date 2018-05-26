import pexpect
import logging

from netconnect.base import BaseDriver
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)


# Settings
logging.basicConfig(level=logging.DEBUG)


class UnixDriver(BaseDriver):
    """
    Driver to login to unix shell devices. Configured for bash shells
    """
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

        self.child = pexpect.spawn(login_cmd)
        i = self.child.expect(PEXPECT_ERRORS + ['[#\$]', '.*assword.*'])
        if i == 0 or i == 1:
            logging.debug('{0} error connecting to device'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('logged in to bash')
            return self.child
        elif i == 3:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + ['[#\$]'])
            if j == 0 or j == 1:
                logging.debug('{0} error sending user password'.format(self.device))
                clean_up_error(self.child, j)
            elif j == 2:
                logging.debug('logged in to bash')

