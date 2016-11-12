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
    """
    Driver to login and send commands to cisco devices.
    """
    @staticmethod
    def enable_mode(child, device, enable_password=''):
        """
        Enter enable mode on device
        :param child: Pexpect spawn child process
        :param device: Device name
        :param enable_password: Enable password if required
        """
        child.sendline('enable')
        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending enable command'.format(device))
            clean_up_error(child, i)
        elif i == 2:
            if not enable_password:
                child.close()
                raise ValueError('Need enable password, but none provided')
            child.sendline(enable_password)
            j = child.expect(PEXPECT_ERRORS + ['.*#'])
            if j == 0 or j == 1:
                logging.debug('{0} error sending enable password'.format(device))
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
            logging.debug('{0} error connecting to device'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + ['.*>', '.*#'])
            if j == 0 or j == 1:
                logging.debug('{0} error sending user password'.format(self.device))
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

        self.child.sendline('terminal length 0')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            logging.debug('{0} error sending disable paging command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} paging disabled'.format(self.device))
            return True

    def save_config(self, source='running-config', destination='startup-config'):
        """
        Save device config
        :param source: Source file name
        :param destination: Destination file name
        :return: True if successful
        """
        self.child.sendcontrol('z')
        self.child.sendline('copy {0} {1}'.format(source, destination))
        i = self.child.expect(PEXPECT_ERRORS + ['.*Destination filename.*', '.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending copy run start command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            self.child.sendcontrol('m')
            j = self.child.expect(PEXPECT_ERRORS + ['.*#'])
            if j == 0 or j == 1:
                logging.debug('{0} error saving config'.format(self.device))
                clean_up_error(self.child, j)
            elif i == 2:
                logging.debug('{0} config saved'.format(self.device))
                return True
        elif i == 3:
            logging.debug('{0} config saved'.format(self.device))
            return True

    def configuration_mode(self):
        """
        Enter configuration mode
        :return: True if successful
        """
        self.child.sendline('configure terminal')
        i = self.child.expect(PEXPECT_ERRORS + ['.*\(config\)#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending configure terminal command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} configuration mode'.format(self.device))
            return True

    def enable_api(self):
        """
        Enable device API. Currently only supported on IOS-XE
        :return:
        """
        pass
