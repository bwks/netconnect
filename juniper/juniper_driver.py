import pexpect
import logging

from netconnect import helpers
from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)

# Settings
logging.basicConfig(level=logging.DEBUG)


class JuniperDriver(BaseLogin):

    @staticmethod
    def operational_mode(child, device):
        """
        Move into operational mode if in root cli
        :param child: pexpect spawn child
        :param device: name of device
        :return: pexpect.spawn child
        """
        child.sendline('cli')
        i = child.expect(PEXPECT_ERRORS + ['.*>'])
        if i == 0 or i == 1:
            clean_up_error(child, i)
        elif i == 2:
            logging.debug('{0} operational mode'.format(device))

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

        self.child = pexpect.spawn(login_cmd, timeout=self.timeout)
        i = self.child.expect(PEXPECT_ERRORS + ['.*assword', '.*:~ #', '@.*%', '.*>'])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + ['.*:~ #', '@.*%', '.*>'])
            if j == 0 or j == 1:
                clean_up_error(self.child, j)
            elif j == 2 or j == 3:
                logging.debug('{0} root user mode'.format(self.device))
                self.operational_mode(child=self.child, device=self.device)
            elif j == 4:
                logging.debug('{0} operational mode'.format(self.device))
        elif i == 3 or i == 4:
            print('3 or 4')
            logging.debug('{0} root user mode'.format(self.device))
            self.operational_mode(child=self.child, device=self.device)
        elif i == 5:
            print(5)
            logging.debug('{0} operational mode'.format(self.device))

    def get_prompt(self):
        return helpers.get_prompt(self.child)

    def send_commands(self, commands, prompt='', disable_paging=True):
        if not prompt:
            prompt = self.get_prompt()

        if disable_paging:
            self.disable_paging(prompt)

        return helpers.send_commands(child=self.child, prompt=prompt, commands=commands)

    def disable_paging(self, prompt=''):
        # expect_prompt = prompt if prompt else '.*>'
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline('set cli screen-length 0')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('paging disabled')
            return True

    def save_config(self):
        self.child.sendline('commit')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('config saved')
            return True

    def configuration_mode(self):
        self.child.sendline('configure')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('configuration mode')
            return True

    def enable_api(self):
        self.child.sendline('set system services netconf ssh')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('netconf ssh enabled')
            return True
