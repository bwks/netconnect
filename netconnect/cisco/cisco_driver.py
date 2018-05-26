import logging
import time
import pexpect

from netconnect import helpers
from netconnect.base import BaseDriver
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS,
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
    EnablePasswordError,
)
from netconnect.constants import (
    PASSWORD_PROMPT,
    CISCO_USER_PROMPT,
    CISCO_PRIV_PROMPT,
    CISCO_CONFIG_PROMPT,
)
from netconnect.messages import (
    send_command_error_msg,
    device_connection_error_msg,
    user_password_error_msg,
    enable_password_error_msg,
    user_exec_success_msg,
    privilege_exec_success_msg,
    configuration_mode_success_msg,
    disable_paging_success_msg,
    save_config_error_msg,
    save_config_success_msg,
)


# Settings
logging.basicConfig(level=logging.DEBUG)


class CiscoDriver(BaseDriver):
    """
    Driver to login and send commands to cisco devices.
    """
    @staticmethod
    def enable_mode(child, device, enable_password='', command='enable'):
        """
        Enter enable mode on device
        :param child: Pexpect spawn child process
        :param device: Device name
        :param enable_password: Enable password if required
        :param command: Command to enter enable mode
        """
        child.sendline(command)
        i = child.expect(PEXPECT_ERRORS + [PASSWORD_PROMPT, CISCO_PRIV_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(device, command))
            clean_up_error(child, i)

        elif i == 2:
            if not enable_password:
                child.close()
                raise EnablePasswordError(
                    '{0} requires enable password, but none provided'.format(device)
                )

            child.sendline(enable_password)
            j = child.expect(PEXPECT_ERRORS + [CISCO_PRIV_PROMPT])

            if j == 0 or j == 1:
                logging.debug(enable_password_error_msg(device))
                clean_up_error(child, j, get_error=False)
                raise EnablePasswordError(enable_password_error_msg(device))

            elif j == 2:
                logging.debug(privilege_exec_success_msg(device))

        elif i == 3:
            logging.debug(privilege_exec_success_msg(device))

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
        i = self.child.expect(
            PEXPECT_ERRORS + [PASSWORD_PROMPT, CISCO_USER_PROMPT, CISCO_PRIV_PROMPT]
        )

        if i == 0 or i == 1:
            logging.debug(device_connection_error_msg(self.device))
            clean_up_error(self.child, i, get_error=False)
            raise LoginTimeoutError(device_connection_error_msg(self.device))

        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + [CISCO_USER_PROMPT, CISCO_PRIV_PROMPT])

            if j == 0 or j == 1:
                logging.debug(user_password_error_msg(self.device))
                clean_up_error(self.child, j, get_error=False)
                raise LoginCredentialsError(user_password_error_msg(self.device))

            elif j == 2:
                logging.debug(user_exec_success_msg(self.device))
                self.enable_mode(self.child, self.device, enable_password)
            elif j == 3:
                logging.debug(privilege_exec_success_msg(self.device))

        elif i == 3:
            self.enable_mode(self.child, self.device, enable_password)

        elif i == 4:
            logging.debug(privilege_exec_success_msg(self.device))

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

    def disable_paging(self, prompt=CISCO_PRIV_PROMPT, command='terminal length 0'):
        """
        Disable paging of long terminal outputs. Represented as <more>
        :param command: Command to disable paging
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

    def save_config(self, source='running-config', destination='startup-config'):
        """
        Save device config
        :param source: Source file name
        :param destination: Destination file name
        :return: True if successful
        """
        command = 'copy {0} {1}'.format(source, destination)

        if self.get_prompt().endswith(')#'):
            self.child.sendline('end')

        self.child.sendline(command)
        # ASA has a timing issue when saving config. Adding
        # in 1 second of sleep before expecting prompt to compensate
        time.sleep(1)
        i = self.child.expect(PEXPECT_ERRORS + ['.*filename.*', CISCO_PRIV_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            self.child.sendcontrol('m')
            j = self.child.expect(PEXPECT_ERRORS + [CISCO_PRIV_PROMPT])

            if j == 0 or j == 1:
                logging.debug(save_config_error_msg(self.device))
                clean_up_error(self.child, j)

            elif i == 2:
                logging.debug(save_config_success_msg(self.device))
                return True

        elif i == 3:
            logging.debug(save_config_success_msg(self.device))
            return True

    def configuration_mode(self, command='configure terminal'):
        """
        :param command: Command to enter config mode
        Enter configuration mode
        :return: True if successful
        """
        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [CISCO_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(configuration_mode_success_msg(self.device))
            return True

    def enable_api(self):
        """
        Enable device API. Currently only supported on IOS-XE
        :return:
        """
        pass
