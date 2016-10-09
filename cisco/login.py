import pexpect
import logging

from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)

# Settings
logging.basicConfig(level=logging.INFO)


class CiscoLogin(BaseLogin):

    @staticmethod
    def enable_mode(child, device, enable_password=''):
        child.sendline('enable')
        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*#'])
        if i == (0 or 1):
            clean_up_error(child, i)
        elif i == 2:
            if not enable_password:
                child.close()
                raise ValueError('Need enable password, but None provided')
            child.sendline(enable_password)
            j = child.expect(PEXPECT_ERRORS + ['.*#'])
            if j == (0 or 1):
                clean_up_error(child, j)
            elif j == 2:
                logging.debug('{0} privilege exec mode'.format(device))
                return child
        elif i == 3:
            logging.debug('{0} privilege exec mode'.format(device))
            return child

    def login(self, login_type='ssh', enable_password=''):
        """
        Login to Cisco IOS, IOS-XE, NXOS
        :param login_type: SSH or Telnet
        :param enable_password: Enable password if required
        :return: pexpect spawn object

        Authentication types:
         - username and password
         - certificate based
        """
        validate_login_type(login_type)

        login_cmd = self.ssh_driver if login_type.lower() == 'ssh' else self.telnet_driver

        child = pexpect.spawn(login_cmd, timeout=self.timeout)
        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*>', '.*#'])
        if i == (0 or 1):
            clean_up_error(child, i)
        elif i == 2:
            child.sendline(self.password)
            j = child.expect(PEXPECT_ERRORS + ['.*>', '.*#'])
            if j == (0 or 1):
                clean_up_error(child, j)
            elif j == 2:
                logging.debug('{0} user exec mode'.format(self.device))
                return self.enable_mode(child=child, device=self.device,
                                        enable_password=enable_password)
            elif j == 3:
                logging.debug('{0} privilege exec mode'.format(self.device))
                return child
        elif i == 3:
            return self.enable_mode(child=child, device=self.device,
                                    enable_password=enable_password)
        elif i == 4:
            logging.debug('{0} privilege exec mode'.format(self.connector.device))
            return child
