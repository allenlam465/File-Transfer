#!/usr/bin/env python
#MD5 with reference to https://en.wikipedia.org/wiki/MD5

#MD5 helper functions #####################################################

#the buffer
#MD5 uses a buffer that is made up of four words that are each 32 bits long

wordA=0x67452301
wordB=0xefcdab89
wordC=0x98badcfe
wordD=0x10325476
#the table
#MD5 uses a table K that has 64 elements. The table is computed beforehand to speed up the computations. The elements are computing using the mathematical sin function: K=abs(sin(i+1))*2^32
#computed this and have a table for it saved (KTable.txt)
#creating K table for MD5 algorithm
kTable=[]
kvalue=open("KTable.txt")
for each in kvalue:
    kTable.append(each)

shiftAmounts=[
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
        ]

#Four Auxiliary Functions
#Each of these functions take three 32-bit words and produce output of one 32 bit word. They apply logical operators to the inputted bits

def F(x,y,z):
    return (x&y)|((~x)&z) 

def G(x,y,z):
    return (x&z) | (y & (~z))

def H(x,y,z):
    return x^y^z

def I(x,y,z):
    return y^(x | ~(z))

#leftrotate function definition
def leftRotate (x,c):
    x&=0xffffffff
    return ((x << c) | (x >> (32-c))) & 0xffffffff

#bytesToInt
def bytesToInt(byteStr):
    return (int(byteStr,2))

def str2Bin(string):
    return ''.join(format(ord(x),'b') for x in string)
#preparing the input####################################################
    #tokenize input
    #split it into 512 bits
#constant declarations
BLOCKSIZE1=512
BLOCKSIZE2=32
INSERTIONBITS=64
def md5():
    #input containers declarations
    with open("data.txt","r") as file:
        data=file.read()
        data=b"The quick brown fox jumps over the lazy dog"
        data=bytearray(data)
        ogLengthInBits=(8*len(data)) & 0xffffffffffffffff
        data.append(0x80) #pre-processing:adding a single 1 bit 
        
        while len(data)%64 != 56: #pre-processing: padding with 0's and adding original length in bits to message
            data.append(0)
        file.close()

    data+=ogLengthInBits.to_bytes(8, byteorder='little')
    hParts=[wordA,wordB,wordC,wordD]
    keepGoing = len(data)

    for blocks in range(0,keepGoing,64):
    #intialize hash value for this chunk:
        A,B,C,D = hParts
        block=data[blocks:blocks+64]
    #Main Loop
        for i in range(0,64):
            if 0 <= i <= 15:
                f=F(B,C,D) 
                g=i
            elif 16 <= i <= 31:
                f=F(D,B,C) 
                g=(5*i + 1) % 16
            elif 32 <= i <= 47:
                f=H(B,C,D) 
                g=(3*i + 5) % 16
            elif 48 <= i <= 63:
                f=I(B,C,D) 
                g=(7*i) % 16
            rotateThis=f+A+int(kTable[i],16)+int.from_bytes(block[4*g:4*g+4],byteorder='little')
            newB=(B+leftRotate(rotateThis,shiftAmounts[i])) & 0xffffffff
            A,B,C,D=D,newB,B,C
    #Add this chunk's hash to result so far:
        for i, val in enumerate([A,B,C,D]):
            hParts[i]+=val
            hParts[i]&=0xffffffff
        digest=[]
        digest=sum(x<<(32*i) for i, x in enumerate(hParts))
   # for each in digest:
   # print(format(each,'x'))
   # print('\n')
    return digest

def md5ToHex(digest):
    raw=digest.to_bytes(16,byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

print(md5ToHex(md5()))
