import logging
import pexpect

from time import strftime

from netconnect import helpers
from netconnect.base import BaseDriver
from netconnect.helpers import (
    clean_up_error,
    PEXPECT_ERRORS,
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
)
from netconnect.constants import (
    PASSWORD_PROMPT,
    VIPTELA_PRIV_PROMPT,
    VIPTELA_CONFIG_PROMPT,
)
from netconnect.messages import (
    send_command_error_msg,
    device_connection_error_msg,
    user_password_error_msg,
    privilege_exec_success_msg,
    configuration_mode_success_msg,
    disable_paging_success_msg,
)

# Settings
logging.basicConfig(level=logging.INFO)


class ViptelaDriver(BaseDriver):
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

        self.child = pexpect.spawn(login_cmd, timeout=self.timeout)
        i = self.child.expect(PEXPECT_ERRORS + [PASSWORD_PROMPT, VIPTELA_PRIV_PROMPT])

        if i == 0 or i == 1:
            logging.debug(device_connection_error_msg(self.device))
            clean_up_error(self.child, i, get_error=False)
            raise LoginTimeoutError(device_connection_error_msg(self.device))

        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + [VIPTELA_PRIV_PROMPT])

            if j == 0 or j == 1:
                logging.debug(user_password_error_msg(self.device))
                clean_up_error(self.child, j, get_error=False)
                raise LoginCredentialsError(user_password_error_msg(self.device))

            elif j == 2:
                logging.debug(privilege_exec_success_msg(self.device))

        elif i == 3:
            logging.debug(privilege_exec_success_msg(self.device))

    def get_prompt(self):
        """
        Attempt to get device prompt
        :return: Device prompt to be used in expects
        """
        return helpers.get_prompt(self.child)

    def send_commands(self, commands, prompt=VIPTELA_PRIV_PROMPT, disable_paging=True):
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

    def disable_paging(self, prompt=VIPTELA_PRIV_PROMPT, command='paginate false'):
        """
        Disable paging of long terminal outputs. Represented as <more>
        :param command: Command to disable pagination
        :param prompt: Prompt to expect
        :return: True if successful
        """
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [prompt])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(disable_paging_success_msg(self.device))
            return True

    def configuration_mode(self, command='configure terminal'):
        """
        Enter configuration mode
        :param command: Command to enter configuration mode
        :return: True if successful
        """
        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [VIPTELA_CONFIG_PROMPT])
        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug(configuration_mode_success_msg(self.device))
            return True

    def config_db_backup(
            self, filename='',
            path='/home/basic',
            prompt=VIPTELA_PRIV_PROMPT,
            timeout=60
            ):
        """
        Backup vManage configuration database. Only valid for vManage devices.
        :param filename: Name of backup file (excluding .tar.gz)
        :param path: Path to save to file
        :param prompt: Expected Prompt
        :param timeout: Timeout in seconds to wait for command to complete
        :return: True if successful
        """
        if not filename:
            time_now = strftime('%Y-%m-%d-%H%M%S')
            filename = '{0}-backup-{1}'.format(self.device, time_now)

        backup_command = 'request nms configuration-db backup path {0}/{1}'.format(path, filename)

        # from somewhere around version 18.X the output of the backup
        # command became very large. The below compensates for that.
        self.child.maxread = 100000000
        self.child.searchwindowsize = 2000

        self.child.sendline(backup_command)
        i = self.child.expect(PEXPECT_ERRORS + [prompt], timeout=timeout)

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, backup_command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug('{0} backup command completed'.format(self.device))
            return True
