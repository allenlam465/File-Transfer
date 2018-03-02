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
                  "c": "1100", "d": "1101", "e": "1110", "f": "1111",}


def file_to_ascii():
    myfile_ascii = ""
    bits = ""
    with open("myfile", "rb") as f:
        # read file by byte
        while True:
            byte = f.read(1)
            if byte == b'':
                break
            byte_hex = byte.hex()
            # split byte into high and low nibbles
            byte_high = byte_hex[:1]
            byte_low = byte_hex[1:2]

            # convert nibbles as hex to bits
            bits += hex_dictionary[byte_high] + hex_dictionary[byte_low]

            # pad bits to be div by 6
            while len(bits)%6 != 0:
                bits += "0"

            # encode bits by 6
            while len(bits) > 0:
                # get 6 bits
                six_bit = bits[:6]
                # convert to int
                mime_encode = int(six_bit, 2)
                # get encoding value
                myfile_ascii += mime_values[mime_encode]
                # substring to next 6 bits
                bits = bits[6:]
    with open("ascii_armored.txt", "w") as f:
        f.write(myfile_ascii)