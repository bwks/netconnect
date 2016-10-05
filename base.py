class Connector(object):
    def __init__(self, device, username='', password='',
                 port=22, ssh_key_file='', ssh_config_file='',
                 ignore_ssh_config=True, ignore_known_hosts=True,
                 host_key_checking=False, timeout=5):

        self.device = device
        self.username = username
        self.password = password
        self.port = port
        self.ssh_key_file = ssh_key_file
        self.ssh_config_file = ssh_config_file
        self.ignore_ssh_config = ignore_ssh_config
        self.ignore_known_hosts = ignore_known_hosts
        self.host_key_checking = host_key_checking
        self.timeout = timeout
        self.prompt = None

        if self.ssh_config_file and not self.ignore_ssh_config:
            self.ssh_driver = 'ssh {0}'.format(self.device)

        else:
            options = ['-p {0}'.format(self.port)]

            if self.username:
                options.append('-l {0}'.format(self.username))

            if self.ignore_known_hosts:
                options.append('-o UserKnownHostsFile=/dev/null')

            if not self.host_key_checking:
                options.append('-o StrictHostKeyChecking=no')

            if self.ssh_key_file:
                options.append('-o IdentityFile={0}'.format(self.ssh_key_file))

            if self.ignore_ssh_config:
                options.append('-F /dev/null')

            self.ssh_driver = 'ssh {0} {1}'.format(' '.join(options), self.device)

        self.telnet_driver = 'telnet {0} {1}'.format(self.device, self.port)
