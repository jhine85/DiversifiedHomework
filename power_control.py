import check_code


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
    power_message_check_code = bytes.fromhex(check_code())  # assuming check_code() returns a string of hex digits
    delimiter = bytes.fromhex('0D')

    # Construct the full message
    message = soh + reserved + monitor_id_byte + message_sender + message_type + message_length + stx + power_control_cmd + power_mode_bytes + etx + power_message_check_code + delimiter

    return message
