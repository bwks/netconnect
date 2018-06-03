import pexpect
import logging

from netconnect.base import BaseDriver
from netconnect import helpers
from netconnect.helpers import (
    validate_login_type,
    clean_up_error,
    PEXPECT_ERRORS
)
from netconnect.constants import (
    UNIX_PROMPT,
    PASSWORD_PROMPT,
)
from netconnect.messages import (
    device_connection_error_msg,
    bash_success_msg,
    user_password_error_msg,
)


# Settings
logging.basicConfig(level=logging.DEBUG)


class UnixDriver(BaseDriver):
    """
    Driver to login to unix shell devices. Configured for bash shells
    """
    def login(self, login_type='ssh'):
        """
        Login to linux/unix shell (bash terminal assumed)
        :param login_type: SSH or Telnet
        :return: pexpect spawn object

        Authentication types:
         - username and password
         - certificate based
        """
        validate_login_type(login_type)

        login_cmd = self.ssh_driver if login_type.lower() == 'ssh' else self.telnet_driver

        self.child = pexpect.spawn(login_cmd)
        i = self.child.expect(PEXPECT_ERRORS + [UNIX_PROMPT, PASSWORD_PROMPT])
        if i == 0 or i == 1:
            logging.debug(device_connection_error_msg(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug(bash_success_msg(self.device))
            return self.child
        elif i == 3:
            self.child.sendline(self.password)
            j = self.child.expect(PEXPECT_ERRORS + [UNIX_PROMPT])
            if j == 0 or j == 1:
                logging.debug(user_password_error_msg(self.device))
                clean_up_error(self.child, j)
            elif j == 2:
                logging.debug(bash_success_msg(self.device))

    def get_prompt(self):
        """
        Attempt to get device prompt
        :return: Device prompt to be used in expects
        """
        return helpers.get_prompt(self.child)

    def send_commands(self, commands, prompt=UNIX_PROMPT):
        """
        Send a list of commands to device
        :param commands: A list of commands to send
        :param prompt: Prompt to expect
        :return: A list of command results
        """
        if not prompt:
            prompt = self.get_prompt()

        return helpers.send_commands(child=self.child, prompt=prompt, commands=commands)
