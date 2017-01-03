import time
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
        # ASA has a timing issue when saving config. Adding
        # in 1 second of sleep before expecting prompt to compensate
        time.sleep(1)

        i = self.child.expect(PEXPECT_ERRORS + [prompt])
        if i == 0 or i == 1:
            logging.debug('{0} error sending disable paging command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} paging disabled'.format(self.device))
            return True

    def enable_scp(self):
        """
        Enable SCP to facilitate secure file transfer to device
        :return: True if successful
        """
        self.configuration_mode()
        self.child.sendline('ssh scopy enable')
        i = self.child.expect(PEXPECT_ERRORS + ['.*\(config\)#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending scp command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            logging.debug('{0} scp enabled'.format(self.device))
            return True

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
        route = '{0} {1} {2} {3}'.format(service, subnet, subnet_mask, interface_name)
        pass

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
        route = 'route management 0.0.0.0 0.0.0.0 10.1.1.1 1'
        pass

    def enable_api(self, port=443):
        """
        Enable ASA API. Must have rest API extensions installed on flash
        :param port: API port number
        :return: True if successful
        """
        self.configuration_mode()
        self.child.sendline('http server enable {0}'.format(port))
        i = self.child.expect(PEXPECT_ERRORS + ['.*\(config\)#'])
        if i == 0 or i == 1:
            logging.debug('{0} error sending http server command'.format(self.device))
            clean_up_error(self.child, i)
        elif i == 2:
            self.child.sendline('rest-api agent')
            j = self.child.expect(PEXPECT_ERRORS + ['.*\(config\)#'])
            if j == 0 or j == 1:
                logging.debug('{0} error rest-api agent command'.format(self.device))
                clean_up_error(self.child, j)
            elif j == 2:
                if 'error' not in j.child.before:
                    logging.debug('{0} rest-api enabled'.format(self.device))
                    return True
                else:
                    return False
