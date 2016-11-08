import pexpect
import logging

from netconnect import helpers
from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS,
)

# Settings
logging.basicConfig(level=logging.DEBUG)


class CiscoDriver(BaseLogin):

    @staticmethod
    def enable_mode(child, device, enable_password=''):
        child.sendline('enable')
        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*#'])
        if i == 0 or i == 1:
            clean_up_error(child, i)
        elif i == 2:
            if not enable_password:
                child.close()
                raise ValueError('Need enable password, but none provided')
            child.sendline(enable_password)
            j = child.expect(PEXPECT_ERRORS + ['.*#'])
            if j == 0 or j == 1:
                clean_up_error(child, j)
            elif j == 2:
                logging.debug('{0} privilege exec mode'.format(device))
        elif i == 3:
            logging.debug('{0} privilege exec mode'.format(device))

    def login(self, login_type='ssh', enable_password=''):
        """
        Login to Cisco IOS, IOS-XE, NXOS
        :param login_type: SSH or Telnet
        :param enable_password: Enable password if required

        Authentication types:
         - username and password
         - certificate based
        """
        validate_login_type(login_type)

        login_cmd = self.ssh_driver if login_type.lower() == 'ssh' else self.telnet_driver

        self.child = pexpect.spawn(login_cmd, timeout=self.timeout)
        i = self.child.expect(PEXPECT_ERRORS + ['.*assword', '.*>', '.*#'])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + ['.*>', '.*#'])
            if j == 0 or j == 1:
                clean_up_error(self.child, j)
            elif j == 2:
                logging.debug('{0} user exec mode'.format(self.device))
                self.enable_mode(child=self.child, device=self.device,
                                 enable_password=enable_password)
            elif j == 3:
                logging.debug('{0} privilege exec mode'.format(self.device))
        elif i == 3:
            self.enable_mode(child=self.child, device=self.device,
                             enable_password=enable_password)
        elif i == 4:
            logging.debug('{0} privilege exec mode'.format(self.device))

    def get_prompt(self):
        return helpers.get_prompt(self.child)

    def send_commands(self, commands, prompt='', disable_paging=True):

        if not prompt:
            prompt = self.get_prompt()

        if disable_paging:
            self.disable_paging(prompt)

        return helpers.send_commands(child=self.child, prompt=prompt, commands=commands)

    def disable_paging(self, prompt=''):
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline('terminal length 0')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('paging disabled')
            return True

    def enable_api(self):
        pass
