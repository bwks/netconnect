import logging

from netconnect.helpers import (
    clean_up_error,
    PEXPECT_ERRORS,
)
from . cisco_driver import CiscoDriver

# Settings
logging.basicConfig(level=logging.DEBUG)


class CiscoASADriver(CiscoDriver):
    """
    Cisco ASA Driver
    """
    def disable_paging(self, prompt=''):
        """
        Disable paging of long terminal outputs. Represented as <more>
        :param prompt: Prompt to expect
        :return: True if successful
        """
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline('terminal pager 0')
        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            logging.debug('{0} error sending disable paging command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} paging disabled'.format(self.device))
            return True
