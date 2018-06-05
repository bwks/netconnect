from netconnect import messages


def test_message_output():
    assert messages.send_command_error_msg('stuff', 'things') == 'stuff error sending "things" command'
