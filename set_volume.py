# Set the volume of a monitor within range 0 to 100
def set_volume(volume_value: int) -> bytes:
    # Start of Message
    stx = bytes.fromhex('02')

    # Operation code page
    op_code_page = bytes.fromhex('00')

    # Operation code
    op_code = bytes.fromhex('62')

    # Set volume value
    set_volume_value = bytes([int(volume_value * 255 / 100)])

    # End of Message
    etx = bytes.fromhex('03')

    # Combine all parts of the message
    message = stx + op_code_page + op_code + set_volume_value + etx

    return message