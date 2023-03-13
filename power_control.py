# check_code function
def check_code():
    # Convert hexadecimal values to binary representation
    bin_list = [bin(int(val, 16))[2:].zfill(8) for val in hex_list]

    # Calculate XOR of binary values
    result = int(bin_list[0], 2)
    for i in range(1, len(bin_list)):
        result ^= int(bin_list[i], 2)

    # Convert result to hexadecimal representation
    hex_result = hex(result)[2:].zfill(2)

    return hex_result


# Construct a message that will send a power on and power off request
# On value is 0001
# Off value is 0004
def construct_power_control_message(monitor_id: str, power_mode: int) -> bytes:
    # Convert monitor ID to hex byte
    monitor_id_byte = bytes([ord(monitor_id) - 16])

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
        monitor_id_byte,
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
    power_message_check_code = check_code(message)

    # Insert the check code into the message list
    message_components.append(bytes.fromhex(power_message_check_code))

    # Add the delimiter to the message list
    message_components.append(delimiter)

    # Convert the message list to a byte string
    message = b''.join(message_components)

    return message
