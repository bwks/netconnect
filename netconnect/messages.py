def send_command_error_msg(device, command):
    return '{0} error sending "{1}" command'.format(device, command)


def device_connection_error_msg(device):
    return '{0} error connecting to device'.format(device)


def user_password_error_msg(device):
    return '{0} error sending user password'.format(device)


def enable_password_error_msg(device):
    return '{0} error sending enable password'.format(device)


def disable_paging_success_msg(device):
    return '{0} paging was disabled'.format(device)


def user_exec_success_msg(device):
    return '{0} entered user exec mode'.format(device)


def privilege_exec_success_msg(device):
    return '{0} entered privilege exec mode'.format(device)


def configuration_mode_success_msg(device):
    return '{0} entered configuration mode'.format(device)


def juniper_shell_mode_success_msg(device):
    return '{0} entered juniper shell mode'.format(device)


def operational_mode_success_msg(device):
    return '{0} entered operational mode'.format(device)


def save_config_error_msg(device):
    return '{0} error saving config'.format(device)


def save_config_success_msg(device):
    return '{0} config saved'.format(device)


def netconf_enabled_success_msg(device):
    return '{0} netconf enabled'.format(device)


def scp_enabled_success_msg(device):
    return '{0} scp enabled'.format(device)


def rest_api_enabled_success_msg(device):
    return '{0} rest api enabled'.format(device)