import pexpect


def get_prompt(child):
    child.sendcontrol('m')
    child.sendcontrol('m')
    prompt = child.before
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


def debug_output(child):
    hashes = '#' * 20
    print('{0} {1} {0}'.format(hashes, 'before', hashes))
    print(child.before)
    print('{0} {1} {0}'.format(hashes, 'after', hashes))
    print(child.after)
    print('{0} {1} {0}'.format(hashes, 'child', hashes))
    print(child)
