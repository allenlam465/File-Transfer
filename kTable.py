#creating K table for MD5 algorithm
#the table
#MD5 uses a table K that has 64 elements. The table is computed beforehand to speed up the computations. The elements are computing using the mathematical sin function: K=abs(sin(i+2))*2^32
#should compute this and have a table for it saved
from math import sin
from math import radians

k=[]

for i in range (0,64):
    k.append(abs(sin(radians(i+2)))*2**32)
    print(k[i])


