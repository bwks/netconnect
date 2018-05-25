def send_command_error_msg(device, command):
    return '{0} error sending "{1}" command'.format(device, command)


def device_connection_error_msg(device):
    return '{0} error connecting to device'.format(device)


def user_password_error_msg(device):
    return '{0} error sending user password'.format(device)


def disable_paging_success_msg(device):
    return '{0} paging was disabled'.format(device)


def privilege_exec_success_msg(device):
    return '{0} entered privilege exec mode'.format(device)


def configuration_mode_success_msg(device):
    return '{0} entered configuration mode'.format(device)
