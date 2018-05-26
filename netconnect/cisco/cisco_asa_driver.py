import time
import logging

from . cisco_driver import CiscoDriver
from netconnect.helpers import (
    clean_up_error,
    PEXPECT_ERRORS,
)
from netconnect.constants import (
    CISCO_CONFIG_PROMPT
)
from netconnect.messages import (
    send_command_error_msg,
    disable_paging_success_msg,
    scp_enabled_success_msg,
    rest_api_enabled_success_msg,
)


# Settings
logging.basicConfig(level=logging.DEBUG)


class CiscoASADriver(CiscoDriver):
    """
    Cisco ASA Driver
    """
    def disable_paging(self, prompt='', command='terminal pager 0'):
        """
        Disable paging of long terminal outputs. Represented as <more>
        :param prompt: Prompt to expect
        :param command: Command to disable paging
        :return: True if successful
        """
        if not prompt:
            prompt = self.get_prompt()

        self.child.sendline(command)
        # ASA has a timing issue when saving config. Adding
        # in 1 second of sleep before expecting prompt to compensate
        time.sleep(1)
        i = self.child.expect(PEXPECT_ERRORS + [prompt])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(disable_paging_success_msg(self.device))
            return True

    def enable_scp(self, command='ssh scopy enable'):
        """
        Enable SCP to facilitate secure file transfer to device
        :return: True if successful
        """
        self.configuration_mode()

        self.child.sendline(command)
        i = self.child.expect(PEXPECT_ERRORS + [CISCO_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, command))
            clean_up_error(self.child, i)

        elif i == 2:
            logging.debug(scp_enabled_success_msg(self.device))
            return True

    # Part of enabling the API, might end up deleting this
    def add_service_route(self, service, subnet, subnet_mask, interface_name):
        """
        Add a service route for example:
          - http 0.0.0.0 0.0.0.0 management
        :param service: Name of service
        :param subnet: Permitted subnet
        :param subnet_mask: Permitted subnet mask
        :param interface_name: Name of interface
        :return: True is successful
        """
        # route = '{0} {1} {2} {3}'.format(service, subnet, subnet_mask, interface_name)
        pass

    # Part of enabling the API, might end up deleting this
    def add_static_route(self, interface_name, subnet, subnet_mask, next_hop):
        """
        Add a static route for example:
          - route management 0.0.0.0 0.0.0.0 10.1.1.1 1
        :param interface_name: Name of interface
        :param subnet: Destination subnet
        :param subnet_mask: Destination subnet mask
        :param next_hop: Next hop IP address
        :return: True if successful
        """
        # route = 'route management 0.0.0.0 0.0.0.0 10.1.1.1 1'
        pass

    def enable_api(self, port=443):
        """
        Enable ASA API. Must have rest API extensions installed on flash
        :param port: API port number
        :return: True if successful
        """
        self.configuration_mode()

        http_enable_cmd = 'http server enable {0}'.format(port)
        self.child.sendline(http_enable_cmd)
        i = self.child.expect(PEXPECT_ERRORS + [CISCO_CONFIG_PROMPT])

        if i == 0 or i == 1:
            logging.debug(send_command_error_msg(self.device, http_enable_cmd))
            clean_up_error(self.child, i)

        elif i == 2:
            rest_api_enable_cmd = 'rest-api agent'
            self.child.sendline(rest_api_enable_cmd)
            j = self.child.expect(PEXPECT_ERRORS + [CISCO_CONFIG_PROMPT])

            if j == 0 or j == 1:
                logging.debug(send_command_error_msg(self.device, rest_api_enable_cmd))
                clean_up_error(self.child, j)

            elif j == 2:
                if 'error' not in j.child.before:
                    logging.debug(rest_api_enabled_success_msg(self.device))
                    return True
                else:
                    return False
