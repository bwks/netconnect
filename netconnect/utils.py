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


def scp(device, username, password, source_file, destination_file, timeout=60,
        scp_port=22, ssh_key_file='', ssh_config_file='',
        ignore_ssh_config=True, ignore_known_hosts=True,
        disable_host_key_checking=False
        ):
    """
    SCP a file from a remote device to the local host.
    :param device: name or IP of remote device
    :param username: user to connect to device
    :param password: users password
    :param source_file: full path to source file
    :param destination_file: full path to destination file
    :param timeout: timeout value for transfer

    :param scp_port: SCP port number
    :param ssh_key_file: SSH key file
    :param ssh_config_file: SSH config file
    :param ignore_ssh_config: Ignore SSH config file
    :param ignore_known_hosts: Ignore SSH known hosts file
    :param disable_host_key_checking: Disable remote host key checking
    :return: True if successful
    """
    if ssh_config_file and ignore_ssh_config:
        raise AttributeError('cannot define ssh_config_file '
                             'and set ignore_ssh_config to True')

    options = []
    if scp_port:
        options.append('-P {0}'.format(scp_port))

    if ignore_known_hosts:
        options.append('-o UserKnownHostsFile=/dev/null')

    if disable_host_key_checking:
        options.append('-o StrictHostKeyChecking=no')

    if ssh_key_file:
        options.append('-o IdentityFile={0}'.format(ssh_key_file))

    if ssh_config_file:
        options.append('-F {0}'.format(ssh_config_file))

    if ignore_ssh_config:
        options.append('-F /dev/null')

    scp_command = 'scp {0} {1}@{2}:{3} {4}'.format(
        ' '.join(options), username, device, source_file, destination_file)

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
