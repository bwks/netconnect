import logging
import pexpect

from netconnect.constants import (
    PASSWORD_PROMPT,
)
from netconnect.helpers import (
    PEXPECT_ERRORS,
    clean_up_error
)
from netconnect.exceptions import (
    LoginTimeoutError,
    LoginCredentialsError,
)
from netconnect.messages import (
    user_password_error_msg,
    device_connection_error_msg,
    scp_success_msg
)


def scp(device, username, password, source_file, destination_file, timeout=60):
    """
    SCP a file from a remote device to the local host.
    :param device: name or IP of remote device
    :param username: user to connect to device
    :param password: users password
    :param source_file: full path to source file
    :param destination_file: full path to destination file
    :param timeout: timeout value for transfer
    :return: True if successful
    """
    scp_command = 'scp {0}@{1}:{2} {3}'.format(
        username, device, source_file, destination_file
    )
    child = pexpect.spawn(scp_command)
    i = child.expect(PEXPECT_ERRORS + [PASSWORD_PROMPT])

    if i == 0 or i == 1:
        logging.debug(device_connection_error_msg(device))
        clean_up_error(child, i, get_error=False)
        raise LoginTimeoutError(device_connection_error_msg(device))

    elif i == 2:
        child.sendline(password)
        j = child.expect(PEXPECT_ERRORS + ['100%'], timeout=timeout)
        if j == 0 or j == 1:
            logging.debug(user_password_error_msg(device))
            clean_up_error(child, j, get_error=False)
            raise LoginCredentialsError(user_password_error_msg(device))

        elif j == 2:
            logging.debug(scp_success_msg(device, source_file, destination_file))
            return True
