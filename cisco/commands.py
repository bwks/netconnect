import logging
from netconnect.helpers import get_prompt, clean_up_error, PEXPECT_ERRORS


def disable_paging(child, prompt=''):
    expect_prompt = prompt if prompt else '.*#'
    child.sendline('terminal length 0')
    i = child.expect(PEXPECT_ERRORS + [expect_prompt])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('paging disabled')
        return True


def enable_iosex_api():
    pass
