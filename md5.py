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

#bytesToInt
def bytesToInt(byte):
    print("bytestoINt")
    print(type(byte))
    print(byte)
    print(int.from_bytes(byte, byteorder='little', signed=False))
    return int.from_bytes(byte, byteorder='little', signed=False)

def str2Bin(string):
    return ''.join(format(ord(x),'b') for x in string)
#preparing the input####################################################
    #tokenize input
    #split it into 512 bits
#constant declarations
BLOCKSIZE1=512
BLOCKSIZE2=32
INSERTIONBITS=64

#input containers declarations
with open("data.txt","r") as file:
    data=file.read()
    data=str2Bin(data)
    print(type(data))
    data+='1'           #pre-processing:adding a single 1 bit  
    ogDataLen=len(data)
    eofPosition=ogDataLen
    while(eofPosition % BLOCKSIZE1 < 448): #pre-processing: padding with 0's and adding original length in bits to message
        data+='0'
        eofPosition+=1
    ogLength="{:b}".format(ogDataLen % 2**INSERTIONBITS)    #original length in bits mod 2^64 ***not sure about thispart
    print(ogLength)
    file.close()
    ogLength=str2Bin(ogLength)
    print("ogLength")
    print(ogLength)
    data+=ogLength
    print(data)
#Process the message in successive 512-bit chunks:
chunkBig=data[:BLOCKSIZE1]
blocks=[]
blockNum=0
keepGoing = len(data)

while keepGoing > 0:
    blocks.append(data[blockNum*BLOCKSIZE1:(blockNum+1)*BLOCKSIZE1])
    keepGoing-=BLOCKSIZE1
for b in blocks:
    M=[]
    for j in range(0, 16):
        chunkSmall=b[j*BLOCKSIZE2:(j+1)*BLOCKSIZE2]
        M.append(chunkSmall)
#intialize hash value for this chunk:
    A=wordA
    B=wordB
    C=wordC
    D=wordD
    print("A:")
    print(A)
    print("B:")
    print(B)
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
        print("f")
        f=f+A+int(kTable[i],16)+bytesToInt(M[g])
        print((M[g]))
        A=D
        D=C
        C=B
        B=B+leftRotate(f,shiftAmounts[i])
        print("C is:")
        print(C)
#Add this chunk's hash to result so far:
    wordA=wordA + A
    wordB=wordB + B
    wordC=wordC + C
    wordD=wordD + D

digest=[]
digest.append(wordA)      #output is in little-endian
digest.append(wordB)
digest.append(wordC)
digest.append(wordD)
for each in digest:
    print(format(each,'x'))
    print('\n')
