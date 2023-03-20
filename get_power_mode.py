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


def get_power_setting(response_bytes):
    """
    Parses a byte response from a monitor device and extracts the power setting information.

    Args:
        response_bytes (bytes): The byte response from the monitor device.

    Returns:
        dict: A dictionary containing the power setting information extracted from the response.
    """
    # Check that the response has the correct length
    if len(response_bytes) != 19:
        raise ValueError("Invalid response length")

    # Extract the result code from the response
    result_code = response_bytes[1:3].decode('ascii')

    # Check if the result code indicates an error
    if result_code != '00':
        raise ValueError("Error response from monitor")

    # Extract the OP code page from the response
    op_code_page = response_bytes[3:5].decode('ascii')

    # Extract the OP code from the response
    op_code = response_bytes[5:7].decode('ascii')

    # Extract the operation type code from the response
    operation_type = response_bytes[7:8].decode('ascii')

    # Extract the maximum value from the response
    max_value = int(response_bytes[8:12].decode('ascii'), 16)

    # Extract the current value from the response
    current_value = int(response_bytes[12:16].decode('ascii'), 16)

    return {
        'op_code_page': op_code_page,
        'op_code': op_code,
        'operation_type': operation_type,
        'max_value': max_value,
        'current_value': current_value
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