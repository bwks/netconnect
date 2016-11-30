import pexpect
import logging

from netconnect import helpers
from netconnect.base import BaseLogin
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
)

# Settings
logging.basicConfig(level=logging.DEBUG)


class JuniperDriver(BaseLogin):
    """
    Driver to login and send commands to juniper devices.
    """
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
            logging.debug('{0} error sending cli command'.format(device))
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
            logging.debug('{0} error connecting to device'.format(self.device))
            clean_up_error(self.child, i, get_error=False)
            raise LoginTimeoutError('{0} error connecting to device'.format(self.device))
        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + ['.*:~ #', '@.*%', '.*>'])
            if j == 0 or j == 1:
                logging.debug('{0} error sending user password'.format(self.device))
                clean_up_error(self.child, j, get_error=False)
                raise LoginCredentialsError('{0} error sending user password'.format(self.device))
            elif j == 2 or j == 3:
                logging.debug('{0} root user mode'.format(self.device))
                self.operational_mode(child=self.child, device=self.device)
            elif j == 4:
                logging.debug('{0} operational mode'.format(self.device))
        elif i == 3 or i == 4:
            logging.debug('{0} root user mode'.format(self.device))
            self.operational_mode(child=self.child, device=self.device)
        elif i == 5:
            logging.debug('{0} operational mode'.format(self.device))

    def get_prompt(self):
        """
        Attempt to get device prompt
        :return: Device prompt to be used in expects
        """
        return helpers.get_prompt(self.child)

    def send_commands(self, commands, prompt='', disable_paging=True):
        """
        Send a list of commands to device
        :param commands: A list of commands to send
        :param prompt: Prompt to expect
        :param disable_paging: Set to True, else make the disable paging
               command the first command in the list
        :return: A list of command results
        """
        if not prompt:
            prompt = self.get_prompt()

        if disable_paging:
            self.disable_paging(prompt)

        return helpers.send_commands(child=self.child, prompt=prompt, commands=commands)

    def disable_paging(self, prompt=''):
        """
        Disable paging of long terminal outputs. Represented as <more>
        :param prompt: Prompt to expect
        :return: True if successful
        """
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline('set cli screen-length 0')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            logging.debug('{0} error sending disable paging command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} paging disabled'.format(self.device))
            return True

    def save_config(self):
        """
        Save device config
        :return: True if successful
        """
        self.child.sendline('commit')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending commit command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} config saved'.format(self.device))
            return True

    def configuration_mode(self):
        """
        Enter configuration mode
        :return: True if successful
        """
        self.child.sendline('configure')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending configure command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} configuration mode'.format(self.device))
            return True

    def enable_api(self):
        """
        Enable device API
        :return: True if successful
        """
        if self.get_prompt().endswith('>'):
            self.configuration_mode()

        self.child.sendline('set system services netconf ssh')
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending enable api command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} netconf ssh enabled'.format(self.device))
            return self.save_config()
