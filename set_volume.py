# Set the volume of a monitor within range 0 to 100
def set_volume(volume_value):
    # Start of Message
    stx = "02h"
    stx_ascii = f"{stx}"

    # Operation code page
    op_code_page = "00h"
    op_code_page_ascii = f"{op_code_page}"

    # Operation code
    op_code = "62h"
    op_code_ascii = f"{op_code}"

    # Set volume value
    set_volume_value_ascii = chr(int(volume_value * 255 / 100))

    # End of Message
    etx = "03h"
    etx_ascii = f"{etx}"

    # Combine all parts of the message
    message = stx_ascii + op_code_page_ascii + op_code_ascii + set_volume_value_ascii + etx_ascii

    return message
