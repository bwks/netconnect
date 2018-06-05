import pexpect


PEXPECT_ERRORS = [pexpect.EOF, pexpect.TIMEOUT]
DEBUG = True


def get_prompt(child):
    child.sendcontrol('m')
    child.expect('.*[>\#\$]')

    result = child.after.decode(encoding='UTF-8')
    if '\x1b[5n' in result:
        split_string = '\x1b[5n'
    elif '\r\n\r\n' in result:
        split_string = '\r\n\r\n'
    elif '\r\n\r' in result:
        split_string = '\r\n\r'
    elif '\r\n' in result:
        split_string = '\r\n'
    else:
        split_string = '\n'

    prompt = result.split(split_string)[-1]
    return prompt


def send_commands(child, prompt, commands=None):
    if commands is None or not isinstance(commands, (str, list)):
        raise ValueError('commands should be a [list, of, commands]')
    elif isinstance(commands, str):
        commands = [commands]

    results = []
    for i in commands:
        child.sendline(i)
        j = child.expect(PEXPECT_ERRORS + [prompt])
        if j == 0 or j == 1:
            clean_up_error(child, j)
        elif j == 2:
            results.append(child.before.decode(encoding='UTF-8'))

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
    else:
        return True


def debug_output(child):
    hashes = '#' * 20
    print('{0} {1} {0}'.format(hashes, 'match', hashes))
    print(child.match)
    print('{0} {1} {0}'.format(hashes, 'before', hashes))
    print(child.before)
    print('{0} {1} {0}'.format(hashes, 'after', hashes))
    print(child.after)
    print('{0} {1} {0}'.format(hashes, 'child', hashes))
    print(child)
    print('{0} {1} {0}'.format(hashes, 'end', hashes))


def clean_up_error(child, error, get_error=True):
    if DEBUG:
        debug_output(child)
    child.close()
    if get_error:
        parse_error(error)


def clean_output(output, highlight_command=False):
    """
    Remove command and trailing prompt from output
    :param output: output to clean
    :param highlight_command:
    :return: String slice between first and lines
    """
    cleaned = output.splitlines()[1:-1]

    if highlight_command:
        hashes = '#' * 20
        command = output.splitlines()[0]
        cleaned.insert(0, '\r\n{0} {1} {2}\r\n'.format(hashes, command, hashes))

    return '\r\n'.join(cleaned)
