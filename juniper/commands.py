import logging
from netconnect.helpers import get_prompt, clean_up_error, PEXPECT_ERRORS


def disable_paging(child, prompt=''):
    expect_prompt = prompt if prompt else '.*>'
    child.sendline('set cli screen-length 0')
    i = child.expect(PEXPECT_ERRORS + [expect_prompt])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('paging disabled')
        return True


def save_config(child):
    child.sendline('commit')
    i = child.expect(PEXPECT_ERRORS + ['.*#'])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('config saved')
        return True


def configuration_mode(child):
    child.sendline('configure')
    i = child.expect(PEXPECT_ERRORS + ['.*#'])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('configuration mode')
        return True


def enable_api(child):
    child.sendline('set system services netconf ssh')
    i = child.expect(PEXPECT_ERRORS + ['.*#'])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('netconf ssh enabled')
        return True
