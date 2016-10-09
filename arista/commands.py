import logging
from netconnect.helpers import send_commands, clean_up_error, PEXPECT_ERRORS


def enable_api(child, protocol='https', port=443):
    protocols = ('http', 'https')
    if protocol not in protocols:
        raise ValueError('protocol must be either: {0}'.format(' '.join(protocols)))

    expect_prompt = '.*\(config.*\)#'
    commands = [
        'configure terminal',
        'management api http-commands',
        'protocol {0} port {1}'.format(protocol, port),
        'no shutdown'
    ]
    return send_commands(child, expect_prompt, commands)


def save_config(child, prompt=''):
    expect_prompt = prompt if prompt else '.*#'

    child.sendcontrol('z')
    i = child.expect(PEXPECT_ERRORS + [expect_prompt])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        child.sendline('copy running-config startup-config')
        j = child.expect(PEXPECT_ERRORS + [expect_prompt])
        if j == (0 or 1):
            clean_up_error(child, j)
        elif j == 2:
            logging.info('Configuration saved')
            return True
