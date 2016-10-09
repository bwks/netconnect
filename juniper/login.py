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


class JuniperLogin(BaseLogin):

    @staticmethod
    def operational_mode(child, device):
        child.sendline('cli')
        i = child.expect(PEXPECT_ERRORS + ['.*>'])
        if i == (0 or 1):
            clean_up_error(child, i)
        elif i == 2:
            logging.debug('{0} operational mode'.format(device))
            return child

    def login(self, login_type='ssh'):
        """
        Login to Juniper Junos
        :param login_type: SSH or Telnet
        :return: pexpect spawn object

        Authentication types:
         - username and password
         - certificate based
        """
        validate_login_type(login_type)

        login_cmd = self.ssh_driver if login_type.lower() == 'ssh' else self.telnet_driver

        child = pexpect.spawn(login_cmd, timeout=self.timeout)
        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*:~ #', '.*>'])
        if i == (0 or 1):
            clean_up_error(child, i)
        elif i == 2:
            child.sendline(self.password)
            j = child.expect(PEXPECT_ERRORS + ['.*:~ #', '.*>'])
            if j == (0 or 1):
                clean_up_error(child, j)
            elif j == 2:
                logging.debug('{0} root user mode'.format(self.device))
                return self.operational_mode(child=child, device=self.device)
            elif j == 3:
                logging.debug('{0} operational mode'.format(self.device))
                return child
        elif i == 3:
            logging.debug('{0} root user mode'.format(self.device))
            return self.operational_mode(child=child, device=self.device)
        elif i == 4:
            logging.debug('{0} operational mode'.format(self.device))
            return child
