class BaseLogin(object):
    """
    Base login class. Device Driver classes will inherit this class
    """
    def __init__(self, device, username='', password='', telnet_port=23,
                 ssh_port=22, ssh_key_file='', ssh_config_file='',
                 ignore_ssh_config=True, ignore_known_hosts=True,
                 disable_host_key_checking=False, timeout=5):

        self.device = device
        self.username = username
        self.password = password
        self.telnet_port = telnet_port
        self.ssh_port = ssh_port
        self.ssh_key_file = ssh_key_file
        self.ssh_config_file = ssh_config_file
        self.ignore_ssh_config = ignore_ssh_config
        self.ignore_known_hosts = ignore_known_hosts
        self.disable_host_key_checking = disable_host_key_checking
        self.timeout = timeout

        self.__child = None

        if self.ssh_config_file and self.ignore_ssh_config:
            raise AttributeError('cannot define ssh_config_file '
                                 'and set ignore_ssh_config to True')

        options_map = {
            self.ssh_port: '-p {0}'.format(self.ssh_port),
            self.username: '-l {0}'.format(self.username),
            self.ignore_known_hosts: '-o UserKnownHostsFile=/dev/null',
            self.disable_host_key_checking: '-o StrictHostKeyChecking=no',
            self.ssh_key_file: '-o IdentityFile={0}'.format(self.ssh_key_file),
            self.ssh_config_file: '-F {0}'.format(self.ssh_config_file),
            self.ignore_ssh_config: '-F /dev/null',
        }

        options = [value for key, value in options_map.items() if key]

        self.ssh_driver = 'ssh {0} {1}'.format(' '.join(options), self.device)

        self.telnet_driver = 'telnet {0} {1}'.format(self.device, self.telnet_port)

    @property
    def child(self):
        return self.__child

    @child.setter
    def child(self, value):
        self.__child = value
