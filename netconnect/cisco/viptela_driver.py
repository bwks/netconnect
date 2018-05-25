import logging
import pexpect

from time import strftime

from netconnect import helpers
from netconnect.base import BaseLogin
from netconnect.helpers import (
    clean_up_error,
    PEXPECT_ERRORS,
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
)


# Settings
logging.basicConfig(level=logging.INFO)


class ViptelaDriver(BaseLogin):
    """
    Driver to login and send commands to Viptela devices.
    """

    def login(self):
        """
        Login to Viptela devices

        Authentication types:
         - username and password
         - certificate based
        """

        login_cmd = self.ssh_driver

        child = pexpect.spawn(login_cmd, timeout=self.timeout)
        self.child = child

        i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error connecting to device'.format(self.device))
            clean_up_error(child, i, get_error=False)
            raise LoginTimeoutError('{0} error connecting to device'.format(self.device))

        elif i == 2:
            child.sendline(self.password)
            j = child.expect(PEXPECT_ERRORS + ['.*#'])
            if j == 0 or j == 1:
                logging.debug('{0} error sending user password'.format(self.device))
                clean_up_error(child, j, get_error=False)
                raise LoginCredentialsError('{0} error sending user password'.format(self.device))
            elif j == 2:
                logging.debug('{0} privilege exec mode'.format(self.device))

        elif i == 3:
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

        self.child.sendline('paginate false')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            logging.debug('{0} error sending disable paging command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} paging disabled'.format(self.device))
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

    def backup_config_db(self, filename='', path='/home/basic'):

        if not filename:
            time_now = strftime('%Y-%m-%d-%H%M%S')
            filename = '{0}-backup-{1}'.format(self.device, time_now)

        backup_command = 'request nms configuration-db backup path {0}/{1}'.format(path, filename)

        self.child.sendline(backup_command)
        i = self.child.expect(PEXPECT_ERRORS + ['.*#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} backup command completed'.format(self.device))
            return True
