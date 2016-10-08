import pexpect


PEXPECT_ERRORS = [pexpect.EOF, pexpect.TIMEOUT]
DEBUG = False


def get_prompt(child):
    child.sendcontrol('m')
    child.sendcontrol('m')

    result = child.after.decode()
    if '\x1b[5n' in result:
        split_string = '\x1b[5n'
    elif '\r\n' in result:
        split_string = '\r\n'
    else:
        split_string = '\n'

    prompt = result.split(split_string)[-1]
    return prompt


def send_commands(child, prompt, commands=None):
    if commands is None or not isinstance(commands, [str, list]):
        raise ValueError('commands should be a [list, of, commands]')
    elif isinstance(commands, str):
        commands = [commands]

    results = []
    for i in commands:
        child.sendline(i)
        child.expect([pexpect.TIMEOUT, pexpect.EOF, prompt])

    return results


def parse_error(error):
    if error == 0:
        raise pexpect.EOF('Got EOF')
    elif error == 1:
        raise pexpect.TIMEOUT('Got Timeout')


def validate_login_type(login_type):
    if login_type.lower() not in ['ssh', 'telnet']:
        raise ValueError('Invalid login type {0}. '
                         'Valid types are ssh and telnet'.format(login_type))


def debug_output(child):
    hashes = '#' * 20
    print('{0} {1} {0}'.format(hashes, 'before', hashes))
    print(child.before)
    print('{0} {1} {0}'.format(hashes, 'after', hashes))
    print(child.after)
    print('{0} {1} {0}'.format(hashes, 'child', hashes))
    print(child)
    print('{0} {1} {0}'.format(hashes, 'end', hashes))


def clean_up_error(child, error):
    if DEBUG:
        debug_output(child)
    child.close()
    parse_error(error)
