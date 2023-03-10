from enum import Enum


class PowerMode(Enum):
    OFF = 0
    ON = 1


def parse_message(message):
    # Remove any whitespace or newline characters from the message
    message = message.strip()

    # Extract the monitor ID from the message
    monitor_id = chr(int(message[3], 16) + 48)

    # Extract the message type from the message
    message_type = message[4]

    # Extract the message length from the message
    message_length = int(message[5])

    # Extract the power mode from the message
    power_mode = message[10:14]

    return {
        'monitor_id': monitor_id,
        'message_type': message_type,
        'message_length': message_length,
        'power_mode': power_mode
    }


def set_power_mode(message):
    parsed_message = parse_message(message)
    power_mode = parsed_message['power_mode']

    if power_mode == '0001':
        return PowerMode.ON
    elif power_mode == '0004':
        return PowerMode.OFF
    else:
        return None
