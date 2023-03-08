hex_list = []

def check_code(hex_list):
    # Convert hexadecimal values to binary representation
    bin_list = [bin(int(val, 16))[2:].zfill(8) for val in hex_list]

    # Calculate XOR of binary values
    result = int(bin_list[0], 2)
    for i in range(1, len(bin_list)):
        result ^= int(bin_list[i], 2)

    # Convert result to hexadecimal representation
    hex_result = hex(result)[2:].zfill(2)

    return hex_result