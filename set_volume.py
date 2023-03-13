import destination_address
import check_code


# Set the volume of a monitor within range 0 to 100
def set_volume(monitor_id: str, volume_mode: int, destination_address_value=None) -> bytes:
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
    message_type = bytes.fromhex('41')
    message_length = bytes.fromhex('30') + bytes.fromhex('43')
    stx = bytes.fromhex('02')
    op_code_page = bytes.fromhex('00')
    op_code = bytes.fromhex('62')
    etx = bytes.fromhex('03')
    delimiter = bytes.fromhex('03')

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
