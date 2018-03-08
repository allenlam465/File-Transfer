# CS380_Project

Group - AppleVictims
Members - Allen Lam, Dylan Nguyen, John Ung, Sai Padmanaban
Date - 3 - 5 - 2018

File transfer tool using python3 with TCP protocols. 

User will run program using a terminal with: 

	python3 tool.py

tool.py is a driver which can become a server, or a client to access the server, and allow account creation to access the server.
Usernames and passwords are salted hashes that are placed in a users.txt to access.  
Uses MD5 hashing to verify integrity of the file transfer, an XOR Cipher to encrypt/decrypt files, and ASCII Armoring can be requested for sent file.
File that are transfered go through a sequence to encrypt it and decrypt it.
	
	File -> MD5 -> XOR MD5 and file chunks -> ASCII Armoring (Optional) -> Decode ASCII Armoring (Optional) -> XOR MD5 and file chunks -> Verify MD5 -> File

User will have 3 tries to login and send the file again. Anymore the server and client will close. 



