from enum import Enum
import check_code
import destination_address


class PowerMode(Enum):
    OFF = 0
    ON = 1


def get_power_status_message(monitor_id: str, power_mode: int) -> bytes:
    # Get destination address for monitor ID
    destination_address_value = destination_address.get_destination_address(monitor_id)
    if destination_address_value is None:
        raise ValueError('Invalid monitor ID')

    # Convert destination address to bytes
    destination_address_byte = bytes([destination_address_value])

    # Define the message components
    soh = bytes.fromhex('01')
    reserved = bytes.fromhex('30')
    message_sender = bytes.fromhex('30')
    message_type = bytes.fromhex('44')
    message_length = bytes.fromhex('30') + bytes.fromhex('43')
    stx = bytes.fromhex('02')
    op_code_page = bytes.fromhex('43 32 30 33 44 36')
    op_code = f'{power_mode:04d}'.encode()
    etx = bytes.fromhex('03')
    delimiter = bytes.fromhex('0D')

    # Create a list of message components
    message_components = [
        soh,
        reserved,
        destination_address_byte,
        message_sender,
        message_type,
        message_length,
        stx,
        op_code_page,
        op_code,
        etx
    ]

    # Convert the list of components to a byte string
    message = b''.join(message_components)

    # Calculate the check code
    power_message_check_code = check_code.check_code(message_components)

    # Insert the check code into the message list
    message_components.append(bytes.fromhex(power_message_check_code))

    # Add the delimiter to the message list
    message_components.append(delimiter)

    # Convert the message list to a byte string
    message = b''.join(message_components)

    return message


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
