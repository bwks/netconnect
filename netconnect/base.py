class BaseDriver(object):
    """
    Base driver class. Device Driver classes will inherit this class
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

        options = []
        if self.ssh_port:
            options.append('-p {0}'.format(self.ssh_port))

        if self.username:
            options.append('-l {0}'.format(self.username))

        if self.ignore_known_hosts:
            options.append('-o UserKnownHostsFile=/dev/null')

        if self.disable_host_key_checking:
            options.append('-o StrictHostKeyChecking=no')

        if self.ssh_key_file:
            options.append('-o IdentityFile={0}'.format(self.ssh_key_file))

        if self.ssh_config_file:
            options.append('-F {0}'.format(self.ssh_config_file))

        if self.ignore_ssh_config:
            options.append('-F /dev/null')

        self.ssh_driver = 'ssh {0} {1}'.format(' '.join(options), self.device)

        self.telnet_driver = 'telnet {0} {1}'.format(self.device, self.telnet_port)

    @property
    def child(self):
        return self.__child

    @child.setter
    def child(self, value):
        self.__child = value

    def scp(self, source_file, destination_location):

        scp_command = 'scp {0} {1}@{2}:{3}/{0}'.format(
            source_file, self.username, self.device, destination_location
        )
        pass
