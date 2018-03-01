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
def bytesToInt(byteStr):
    print("bytestoINt")
    print(type(byteStr))
    print("byteStr")
    print(byteStr)
    print(int(byteStr,2))
    #hexval="0x%x"%(int(byteStr,2))
    hexval=hex(int(byteStr,2))
    print("hexval")
    print(type(int(byteStr,2)))
    return hexval

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
    print(data)
    data=str2Bin(data)
    print("data")
    print(data)
    ogDataLen=len(data)
    data+='1'           #pre-processing:adding a single 1 bit  
    eofPosition=ogDataLen+1
    while(eofPosition % BLOCKSIZE1 < 448): #pre-processing: padding with 0's and adding original length in bits to message
        data+='0'
        eofPosition+=1
    print(ogDataLen % 2**INSERTIONBITS)
    print("ogLength")
    ogLength="{:064b}".format(ogDataLen % 2**INSERTIONBITS)    #original length in bits mod 2^64 ***not sure about thispart
    print(ogLength)
    file.close()
    data+=ogLength
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
        f=f+A+int(kTable[i],16)+bytesToInt(M[g])
        A=D
        D=C
        C=B
        B=B+leftRotate(f,shiftAmounts[i])
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
