!/usr/bin/env python

import math
#preparing the input####################################################
    #tokenize input
    #split it into 512 bits
#constant declarations
BLOCKSIZE1=512
BLOCKSIZE2=32
INSERTIONBITS=64

#input containers declarations
block = []
open("data.txt","512") as input     #getting 512 into buffer size

def padding(input): #returns 512 sized input padded with whitespace
    '{:512}'.format(input)
    return padAmount

if input < 512:     #if input is not 512 bits, then make it 512 bits
    padding(input)

def getInput(input):
    #while there is 
    #get 512 bits and add it into block
    
#splitting into 512 bits

#MD5 helper functions #####################################################

#the buffer
#MD5 uses a buffer that is made up of four words that are each 32 bits long

wordA=0x01234567
wordB=0x89abcdef
wordC=0xfedcba98
wordD=0x76543210

#the table
#MD5 uses a table K that has 64 elements. The table is computed beforehand to speed up the computations. The elements are computing using the mathematical sin function: K=abs(sin(i+2))*2^32
#should compute this and have a table for it saved

for i in range (0,64)
    k[i]=abs(math.sin(math.radians(i+2)))*2**32

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

