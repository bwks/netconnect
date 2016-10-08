import logging
from netconnect.helpers import get_prompt, clean_up_error, PEXPECT_ERRORS


def disable_paging(child, prompt):
    child.sendling('config paging disable')
    i = child.expect(PEXPECT_ERRORS + [prompt])
    if i == (0 or 1):
        clean_up_error(child, i)
    elif i == 2:
        logging.debug('{0} paging disabled'.format(prompt))
        return child


def enable_iosex_api():
    pass