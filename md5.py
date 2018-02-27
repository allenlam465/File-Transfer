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
kTable=[]
kvalue=open("KTable.txt")
for each in kvalue:
    kTable.append(each)
#    print(each)

shiftAmounts=[
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
        ]

#Four Auxiliary Functions
#Each of these functions take three 32-bit words and produce output of one 32 bit word. They apply logical operators to the inputted bits

def F(x,y,z):
    return (x&y) | ((~x) & z)

def G(x,y,z):
    return (x&z) | (y & (~z))

def H(x,y,z):
    return x^y^z

def I(x,y,z):
    return y^(x | ~(z))

#leftrotate function definition
def leftRotate (x,c):
    return (x << c) | (x >> (32-c))

#preparing the input####################################################
    #tokenize input
    #split it into 512 bits
#constant declarations
BLOCKSIZE1=512
BLOCKSIZE2=32
INSERTIONBITS=64

#input containers declarations
block = []
with open("data.txt","ab+") as file:
    file.write(b'1')        #pre-processing:adding a single 1 bit    
    eofPosition=file.tell()
    while(eofPosition % 512 < 448): #pre-processing: padding with 0's and adding original length in bits to message
        file.write(b'0')
        eofPosition=file.tell()
    ogLength='{0:b}'.format(eofPosition) % 2**64    #original length in bits mod 2^64 ***not sure about thispart
    file.write('{0:b}'.format(ogLength))
    file.close()
#Process the message in successive 512-bit chunks:
file=open("data.txt","rb")
chunkbig=file.read(512)
for chunkBig in file:
    M=[]
    for j in range(0, 16):
        chunkSmall=chunkBig[j*32:32+j*32]
        M.append(chunkSmall)
#intialize hash value for this chunk:
    A=wordA
    B=wordB
    C=wordC
    D=wordD
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
        f=f+A+k[i]+M[g]
        A=D
        D=C
        C=B
        B=B+leftRotate(f,s[i])
    chunkBig=file.read(512)
#Add this chunk;s hash to result so far:
    wordA=wordA + A
    wordB=wordB + B
    wordC=wordC + C
    wordD=wordD + D
digest=[]
digest.append(wordA+wordB+wordC+wordD)      #output is in little-endian
for each in digest:
    print(each)
