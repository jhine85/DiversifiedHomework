import destination_address
import check_code


# Construct a message that will send a power on and power off request
# On value is 0001
# Off value is 0004
def construct_power_control_message(monitor_id: str, power_mode: int, destination_address_value=None) -> bytes:
    # Get destination address for monitor ID
    destination_address_value = destination_address_value.get_destination_address(monitor_id)
    if destination_address_value is None:
        raise ValueError('Invalid monitor ID')

    # Convert destination address to bytes
    destination_address_byte = bytes([destination_address_value])

    # Define the message components
    soh = bytes.fromhex('01')
    reserved = bytes.fromhex('30')
    message_sender = bytes.fromhex('30')
    message_type = bytes.fromhex('41')
    message_length = bytes.fromhex('30') + bytes.fromhex('43')
    stx = bytes.fromhex('02')
    power_control_cmd = bytes.fromhex('43 32 30 33 44 36')
    power_mode_bytes = f'{power_mode:04d}'.encode()
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
        power_control_cmd,
        power_mode_bytes,
        etx
    ]

    # Convert the list of components to a byte string
    message = b''.join(message_components)

    # Calculate the check code
    power_message_check_code = check_code.check_code(message)

    # Insert the check code into the message list
    message_components.append(bytes.fromhex(power_message_check_code))

    # Add the delimiter to the message list
    message_components.append(delimiter)

    # Convert the message list to a byte string
    message = b''.join(message_components)

    return message
