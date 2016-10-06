import pexpect

import logging
logging.basicConfig(level=logging.DEBUG)

from . import helpers


PEXPECT_ERRORS = [pexpect.EOF, pexpect.TIMEOUT]
DEBUG = False


def validate_login_type(login_type):
    if login_type.lower() not in ['ssh', 'telnet']:
        raise ValueError('Invalid login type {0}. '
                         'Valid types are ssh and telnet'.format(login_type))


def clean_up_error(child, error):
    if DEBUG:
        helpers.debug_output(child)
    child.close()
    helpers.parse_error(error)


def enable_mode(child, enable_password, device):
    child.sendline('enable')
    i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*#'])
    if i == (0 or 1):
        clean_up_error(child, a)
    elif i == 2:
        if not enable_password:
            child.close()
            raise ValueError('Need enable password, but None provided')
        child.sendline(enable_password)
        j = child.expect(PEXPECT_ERRORS + ['.*#'])
        if j == (0 or 1):
            clean_up_error(child, b)
        elif j == 2:
            logging.debug('{0} privilege exec mode'.format(device))
            return child
    elif i == 3:
        logging.debug('{0} privilege exec mode'.format(device))
        return child


def unix_login(connector, login_type='ssh'):
    """
    Login to linux/unix shell (bash terminal assumed)
    :param connector: Connector object
    :param login_type: SSH or Telnet
    :return: pexpect spawn object

    Authentication types:
     - username and password
     - certificate based
    """
    validate_login_type(login_type)

    login_cmd = connector.ssh_driver if login_type.lower() == 'ssh' else connector.telnet_driver

    child = pexpect.spawn(login_cmd)
    i = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*$', '.*assword.*'])
    if i == (0 or 1):
        raise i
    elif i == (2 or 3):
        return child
    elif i == 4:
        child.sendline(connector.password)
        j = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*$'])
        if j == (0 or 1):
            raise i
        elif j == (2 or 3):
            return child


def cisco_login(connector, login_type='ssh', enable_password=''):
    """
    Login to Cisco IOS, IOS-XE, NXOS
    :param connector: Connector object
    :param login_type: SSH or Telnet
    :param enable_password: Enable password if required
    :return: pexpect spawn object

    Authentication types:
     - username and password
     - certificate based
    """
    validate_login_type(login_type)

    login_cmd = connector.ssh_driver if login_type.lower() == 'ssh' else connector.telnet_driver

    child = pexpect.spawn(login_cmd, timeout=connector.timeout)
    i = child.expect(PEXPECT_ERRORS + ['.*assword', '.*>', '.*#'])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        child.sendline(connector.password)
        j = child.expect(PEXPECT_ERRORS + ['.*>', '.*#'])
        if j == (0 or 1):
            clean_up_error(child, j)
        elif j == 2:
            logging.debug('{0} user exec mode'.format(connector.device))
            return enable_mode(child, enable_password, connector.device)
        elif j == 3:
            logging.debug('{0} privilege exec mode'.format(connector.device))
            return child
    elif i == 3:
        return enable_mode(child, enable_password, connector.device)
    elif i == 4:
        logging.debug('{0} privilege exec mode'.format(connector.device))
        return child


def arista_login(connector, login_type='ssh', enable_password=''):
    return cisco_login(connector=connector, login_type=login_type,
                       enable_password=enable_password)


def juniper_login():
    pass
