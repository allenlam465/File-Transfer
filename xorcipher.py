from itertools import cycle


def getKey(key):
    with open(key, "rb") as f:
        while True:
            c = f.read(1024)
            if not c:
                f.seek(0)
                c = f.read(1)
            for x in c:
                yield x


def getKeyString(key):
    with open(key, "r") as f:
        while True:
            c = f.read(1024)
            if not c:
                f.seek(0)
                c = f.read(1)
            for x in c:
                yield x


def getFile(input):
    with open(input, "rb") as f:
        while True:
            c = f.read(1024)
            if not c:
                break
            for x in c:
                yield x


def xor(data, key):
    return bytes(a ^ b for a, b in zip(data, cycle(key)))


def encodeDecodeFile(input, output, key):
    with open(input, "rb") as encry, open(output, 'wb') as decry:
        decry.write(xor(encry.read(), getKey(key)))


def xorString(string, key):
    if isinstance(string, str):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(string, getKeyString(key)))
    else:
        return bytes([a ^ b for a, b in zip(string, getKey(key))])


# encode contents to output.txt
# encodeDecodeFile("1.jpg", "1output.jpg", "key.txt")
# decode contents to decodedinput.txt
# encodeDecodeFile("1output.jpg", "decodedinput.jpg", "key.txt")
