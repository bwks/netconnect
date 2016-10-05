import pexpect

import logging
logging.basicConfig(level=logging.DEBUG)

from . import helpers


def validate_login_type(login_type):
    if login_type.lower() not in ['ssh', 'telnet']:
        raise ValueError('Invalid login type {0}. '
                         'Valid types are ssh and telnet'.format(login_type))


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
    i = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*assword', '.*>'])
    if i == (0 or 1):
        helpers.debug_output(child)
        helpers.parse_error(i)
    elif i == 2:
        return child
    elif i == 3:
        child.sendline(connector.password)
        j = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*>'])
        if j == (0 or 1):
            raise i
        elif j == 2:
            return child
        elif j == 3:
            if not enable_password:
                raise ValueError('Need enable password, but None provided')
            child.sendline(enable_password)
            k = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#'])
            if k == (0 or 1):
                raise k
            elif k == 2:
                return child
    elif i == 4:
        if not enable_password:
            raise ValueError('Need enable password, but None provided')
        child.sendline(enable_password)
        j = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#'])
        if j == (0 or 1):
            raise j
        elif j == 2:
            return child

def juniper_login():
    pass


def arista_login():
    pass
