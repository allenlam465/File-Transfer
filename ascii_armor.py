ascii_values = [" ", "!", "\"", "#", "$", "%", "&", "\'",
                "(", ")", "*", "+", ",", "-", ".", "/", "0",
                "1", "2", "3", "4", "5", "6", "7", "8", "9",
                ":", ";", "<", "=", ">", "?", "@", "A", "B",
                "C", "D", "E", "F", "G", "H", "I", "J", "K",
                "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
                "^", "_", "`", "a", "b", "c", "d", "e", "f",
                "g", "h", "i", "j", "k", "l", "m", "n", "o",
                "p", "q", "r", "s", "t", "u", "v", "w", "x",
                "y", "z", "{", "|", "}", "~"]

mime_values = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
               "J", "K", "L", "M", "N", "O", "P", "Q", "R",
               "S", "T", "U", "V", "W", "X", "Y", "Z", "a",
               "b", "c", "d", "e", "f", "g", "h", "i", "j",
               "k", "l", "m", "n", "o", "p", "q", "r", "s",
               "t", "u", "v", "w", "x", "y", "z", "0", "1",
               "2", "3", "4", "5", "6", "7", "8", "9", "+",
               "/"]

hex_values = ["a", "b", "c", "d", "e", "f"]

hex_dictionary = {"0": "0000", "1": "0001", "2": "0010", "3": "0011",
                  "4": "0100", "5": "0101", "6": "0110", "7": "0111",
                  "8": "1000", "9": "1001", "a": "1010", "b": "1011",
                  "c": "1100", "d": "1101", "e": "1110", "f": "1111", }


def file_to_ascii(fileName):
    bits = ""
    with open(fileName, "rb") as f:
        # read file by byte
        while True:
            byte = f.read(1)
            if byte == b'':
                break
            byte_hex = byte.hex()
            # split byte into high and low nibbles
            byte_high = byte_hex[:1]
            byte_low = byte_hex[1:2]
            # convert nibbles as hex to bits array
            bits += hex_dictionary[byte_high] + hex_dictionary[byte_low]
    myfile_ascii = mime_encode(bits)
    with open("ascii_armored.txt", "w") as f:
        f.write(myfile_ascii)


def mime_encode(binary_input):
    ret = ""
    # pad input to be div by 6
    while len(binary_input) % 6 != 0:
        binary_input += "0"
    # encode bits by 6
    while len(binary_input) > 0:
        # get 6 bits
        six_bit = binary_input[:6]
        # convert to int
        mime_index = int(six_bit, 2)
        # get encoding value
        ret += mime_values[mime_index]
        # substring to next 6 bits
        binary_input = binary_input[6:]
    return ret


def ascii_to_file(fileName):
    with open(fileName, "r") as f:
        str_file = f.read()
    hex_string = mime_decode(str_file)
    bytes_to_write = bytearray.fromhex(hex_string)
    with open("byte_decoded", "wb") as f:
        f.write(bytes_to_write)


def mime_decode(str_input):
    ret = ""
    bits = ""
    # read each ASCII char
    for c in str_input:
        # get byte-integer representation of the MIME char
        b = mime_values.index(c)
        # convert that int to binary
        bits += int_to_bits(b)[2:]
    # pad input to be div by 8
    while len(bits) % 8 != 0:
        bits += "0"
    while len(bits) > 0:
        # decode 8 bits at a time
        eight_bits = int(bits[:8])
        # get hex representation of byte
        ret += binary_to_hex(eight_bits) + " "
        # substring bits for next 8
        bits = bits[8:]
    last_byte = ret[len(ret) - 4:]
    if last_byte.strip() == "00":
        return ret[:len(ret) - 4]
    else:
        return ret


def int_to_bits(int_input):
    bits_value = ''
    # convert int to bits, max range 8 bits
    for i in range(8):
        remainder = int_input % 2
        int_input = int_input // 2
        bits_value += str(remainder)

    # reverse order
    return bits_value[::-1]


# takes binary as an int instead of string
def binary_to_hex(bin_input):
    hex_ints = [1, 2, 4, 8]
    hex_val0 = 0
    hex_val1 = 0

    # convert int to hex
    for i in range(8):
        if i > 3:
            j = i - 4
        else:
            j = i
        if bin_input % 10 == 1:
            if i < 4:
                hex_val0 += hex_ints[j]
            else:
                hex_val1 += hex_ints[j]
        bin_input = bin_input // 10
        hex_string = ""
        if hex_val1 > 9:
            hex_string += hex_values[hex_val1 - 10]
        else:
            hex_string += str(hex_val1)
        if hex_val0 > 9:
            hex_string += hex_values[hex_val0 - 10]
        else:
            hex_string += str(hex_val0)
    return hex_string
