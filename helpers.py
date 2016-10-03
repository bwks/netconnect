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
