def getKey(key):
    with open(key, encoding="utf-8", newline="") as f:
        while True:
            c = f.read(1024)
            if not c:
                f.seek(0)
                c = f.read(1)
            for x in c:
                yield x

def getFile(input):
    with open(input, encoding="utf-8", newline="") as f:
        while True:
            c = f.read(1024)
            if not c:
                break
            for x in c:
                yield x

def encodeDecode(input, output, key):
    with open(output, mode="w", encoding="utf-8", newline="") as f:
        for c, d in zip(getFile(input), getKey(key)):
            #print("-->", ord(c), ord(d), ord(a))
            f.write(chr(ord(c)^ord(d)))

#encodeDecode("input.txt", "output.txt", "key.txt") #encode contents to output.txt
encodeDecode("output.txt", "decodedinput.txt", "key.txt") #decode contents to decodedinput.txt