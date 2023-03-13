# EXAMPLE List [30, 41, 30, 45, 30, 41, 02, 30, 30, 31, 30, 30, 30, 36, 34, 03] returns 77


def check_code(message_components):
    # Convert hexadecimal values to binary representation
    bin_list = [bin(int(val, 16))[2:].zfill(8) for val in message_components]

    # Calculate XOR of binary values
    result = int(bin_list[0], 2)
    for i in range(1, len(bin_list)):
        result ^= int(bin_list[i], 2)

    # Convert result to hexadecimal representation
    hex_result = hex(result)[2:].zfill(2)

    return hex_result
