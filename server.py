#!/usr/bin/env python

import socket
import getpass
import hashlib
import crypt
import time
from md5 import md5, md5ToHex
from xorcipher import encodeDecodeFile, xorString
from ascii_armor import file_to_ascii, ascii_to_file


class Server:

    server = None
    host = None
    port = None
    md5 = None
    md5Recv = None

    def __init__(self):  # creates the class object.
        pass

    def startSocket(self):
        # Start socket protocols
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()  # Obtain host name
        self.port = 12345  # Port that it uses
        self.server.bind((self.host, self.port))  # binds a socket to address

    # login stored as user/salt/hashed_password
    def createAcc(self):
        user = input("Input new user:")
        pw = getpass.getpass()
        salt = crypt.mksalt(crypt.METHOD_SHA512)
        hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
        token = user + "/" + salt + "/" + hashed_password

        with open("user.txt", "a") as myFile:
            myFile.write(token)
            myFile.write("\n")

    def checkLogin(self, token):
        fileName = "users.txt"
        file = open(fileName, "r")
        with open(fileName) as f:
            for line in f.readlines():
                split = line.split("/")
                if token.strip() == split[0].strip():
                    return split[1]  # return salt

        print("Invalid username.")
        return -1

    def checkAuthen(self, token):
        fileName = "users.txt"
        file = open(fileName, "r")

        with open(fileName) as f:
            for line in f.readlines():
                if(token.strip() == line.strip()):
                    print("Authorized user.")
                    return True

        print("Invalid username or password.")
        return False

    def utf8len(s):
        return len(s.encode('utf-8'))

    def getMD5Key(self, fileName):
        return md5ToHex(md5(fileName))

    def md5Integrity(self):
        print(self.md5)
        print(self.md5Recv)
        return str(self.md5) == str(self.md5Recv)

    def xorCipherString(self, string):
        return xorString(string, "key.txt")

    def xorFile(self, fileName):
        encodeDecodeFile(fileName, "xor" + fileName, "key.txt")

    def asciiArmorDecode(self, fileName):
        ascii_to_file(fileName)

    def serverClose(self):
        self.server.close()  # Close server

    def main(self):
        self.server.listen(5)  # Listen for 5 connections
        print("Listening for client.")

        # accept connection in the bound socket
        (client, addr) = self.server.accept()
        print("Got connection from ", addr)

        tries = 3

        while(tries != 0):
            # receive username from client
            login_token = (client.recv(1024).decode('utf-8'))

            # return salt to client
            salt = self.checkLogin(login_token)

            if salt == -1:
                # invalid username subtract 1 try
                client.send(bytes("0", 'utf-8'))
                token = ""
            else:
                client.send(bytes(salt, 'utf-8'))
                # receive password hash from client
                pw_token = (client.recv(1024).decode('utf-8')).strip()

                # concat login/salt/pw
                token = login_token + "/" + salt + "/" + pw_token

                print("Checking authorization.")

            if(self.checkAuthen(token)):
                client.send(bytes("1", 'utf-8'))
                time.sleep(0.25)

                client.send(bytes("Thank you for connecting.", 'utf-8'))
                while (tries != 0):
                    client.settimeout(20)
                    self.md5Recv = client.recv(1024).decode('utf-8')
                    self.md5Recv = self.xorCipherString(self.md5Recv)

                    armored = (client.recv(1024).decode('utf-8')).strip()

                    print(armored)

                    if(armored == "1"):
                        client.settimeout(2)
                        try:
                            print("ASCII armoring was applied removing.")
                            with open('received_file', 'wb') as f:
                                print("Opened file.")
                                while True:
                                    data = client.recv(512)
                                    if not data:
                                        break
                                    f.write(data)
                            f.close()
                            self.asciiArmorDecode('received_file')
                            print("ASCII armoring was removed.")

                            print("Applying XOR cipher.")
                            self.xorFile("byte_decoded")
                            print("Finished.")

                            print("Applying MD5.")
                            self.md5 = self.getMD5Key("xorbyte_decoded")
                            print("Finished.")

                        except socket.timeout:
                            self.asciiArmorDecode('received_file')
                            print("ASCII armoring was removed.")

                            print("Applying XOR cipher.")
                            self.xorFile('received_file')
                            print("Finished.")

                            print("Applying MD5.")
                            self.md5 = self.getMD5Key('received_file')
                            print("Finished.")
                    else:
                        print("ASCII armoring was not applied.")

                        client.settimeout(5)
                        try:
                            with open('received_file', 'wb') as f:
                                print("Opened file.")
                                while True:
                                    data = client.recv(1024)
                                    if not data:
                                        break
                                    f.write(data)
                            f.close()

                            print("Applying XOR cipher.")
                            self.xorFile('received_file')
                            print("Finished.")

                            print("Applying MD5.")
                            self.md5 = self.getMD5Key('received_file')
                            print("Finished.")

                        except socket.timeout:
                            print("Applying XOR cipher.")
                            self.xorFile('received_file')
                            print("Finished.")

                            print("Applying MD5.")
                            self.md5 = self.getMD5Key('received_file')
                            print("Finished.")

                    print("Checking MD5.")

                    success = self.md5Integrity()

                    if(success):
                        client.send(bytes("1", 'utf-8'))
                        break
                    else:
                        client.send(bytes("0", 'utf-8'))
                        tries -= 1
                break
            else:
                tries -= 1
                if tries == 0:
                    client.send(bytes("-1", 'utf-8'))
                    client.send(
                        bytes("Too many tries server closing.", 'utf-8'))
                    break
                else:
                    client.send(bytes("0", 'utf-8'))
                    line = "Number tries left: " + str(tries)
                    client.send(bytes(line, 'utf-8'))

        client.send(bytes("Server closing connection.", 'utf-8'))
        time.sleep(1)
        print((client.recv(1024).decode('utf-8')))
        self.serverClose()
