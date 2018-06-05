import pexpect
import logging

from netconnect import helpers
from netconnect.base import BaseDriver
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
)
from netconnect.constants import (
    PASSWORD_PROMPT,
    JUNIPER_OPER_PROMPT,
    JUNIPER_CONFIG_PROMPT,
    JUNIPER_SHELL_PROMPT,
    JUNIPER_ALT_SHELL_PROMPT,
)
from netconnect.messages import (
    send_command_error_msg,
    operational_mode_success_msg,
    device_connection_error_msg,
    user_password_error_msg,
    juniper_shell_mode_success_msg,
    disable_paging_success_msg,
    save_config_success_msg,
    configuration_mode_success_msg,
    netconf_enabled_success_msg,
)

# Settings
logging.basicConfig(level=logging.DEBUG)


class JuniperDriver(BaseDriver):
    """
    Driver to login and send commands to juniper devices.
    """
    @staticmethod
    def operational_mode(child, device, command='cli'):
        """
        Move into operational mode if in root cli
        :param child: pexpect spawn child
        :param device: name of device
        :param command: Command to enter operational mode
        :return: pexpect.spawn child
        """
        child.sendline(command)
        i = child.expect(PEXPECT_ERRORS + [JUNIPER_OPER_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(device, command))
            clean_up_error(child, i)

        elif i == 2:
            logging.debug(operational_mode_success_msg(device))

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
        i = self.child.expect(PEXPECT_ERRORS + [
            PASSWORD_PROMPT, JUNIPER_ALT_SHELL_PROMPT, JUNIPER_SHELL_PROMPT, JUNIPER_OPER_PROMPT
        ])

        if i == 0 or i == 1:
            logging.debug(device_connection_error_msg(self.device))
            clean_up_error(self.child, i, get_error=False)
            raise LoginTimeoutError(device_connection_error_msg(self.device))

        elif i == 2:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + [
                JUNIPER_ALT_SHELL_PROMPT, JUNIPER_SHELL_PROMPT, JUNIPER_OPER_PROMPT
            ])

            if j == 0 or j == 1:
                logging.debug(user_password_error_msg(self.device))
                clean_up_error(self.child, j, get_error=False)
                raise LoginCredentialsError(user_password_error_msg(self.device))

            elif j == 2 or j == 3:
                logging.debug(juniper_shell_mode_success_msg(self.device))
                self.operational_mode(child=self.child, device=self.device)

            elif j == 4:
                logging.debug(operational_mode_success_msg(self.device))

        elif i == 3 or i == 4:
            logging.debug(juniper_shell_mode_success_msg(self.device))
            self.operational_mode(child=self.child, device=self.device)

        elif i == 5:
            logging.debug(operational_mode_success_msg(self.device))

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

    def disable_paging(self, prompt='', command='set cli screen-length 0'):
        """
        Disable paging of long terminal outputs. Represented as <more>
        Paging is disabled from operational mode (>).
        :param prompt: Prompt to expect
        :param command: Command to disable paging
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

    def save_config(self, command='commit'):
        """
        Save device config
        :return: True if successful
        """
        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [JUNIPER_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(save_config_success_msg(self.device))
            return True

    def configuration_mode(self, command='configure'):
        """
        Enter configuration mode
        :param command: Command to enter configuration mode
        :return: True if successful
        """
        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [JUNIPER_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(configuration_mode_success_msg(self.device))
            return True

    def enable_api(self, command='set system services netconf ssh'):
        """
        Enable device API
        :return: True if successful
        """
        if self.get_prompt().endswith('>'):
            self.configuration_mode()

        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [JUNIPER_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(netconf_enabled_success_msg(self.device))
            return self.save_config()
