import pexpect


def unix_login(connection, login_cmd):
    child = pexpect.spawn(login_cmd)
    i = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*$', '.*assword.*'])
    if i == (0 or 1):
        raise i
    elif i == (2 or 3):
        return child
    elif i == 4:
        child.sendline(connection.password)
        j = child.expect([pexpect.EOF, pexpect.TIMEOUT, '.*#', '.*$'])
        if j == (0 or 1):
            raise i
        elif j == (2 or 3):
            return child


def cisco_login():
    pass


def juniper_login():
    pass


def arista_login():
    pass
