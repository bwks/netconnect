from netconnect.cisco.cisco_driver import CiscoDriver


class AristaDriver(CiscoDriver):
    """
    Driver to login and send commands to cisco devices.
    """
    def enable_api(self, https_port=443):
        """
        Enable device API.
        :return:
        """
        commands = ['management api http-commands',
                    'protocol https {0}'.format(https_port),
                    'no shutdown']

        self.configuration_mode()
        self.send_commands(commands=commands, prompt='.*api-http-cmds\)#', disable_paging=False)
        self.save_config()
