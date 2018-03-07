#!/usr/bin/env python

import socket
import getpass
import hashlib
import time
import os
from md5 import md5, md5ToHex
from xorcipher import encodeDecodeFile, xorString
from ascii_armor import file_to_ascii, ascii_to_file, bytes_to_bits


class Client:

    server = None
    host = None
    port = None

    def __init__(self):  # creates the class object.
        pass

    # def startSocket(self,ipAddress)
    def startSocket(self):
        # Start socket protocols
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()  # Obtain host name
        self.port = 12345  # Port that it uses
        self.server.settimeout(10)
        self.server.connect((self.host, self.port))
        # while(True):
        #     self.host = ipAddress  # Obtain host name
        #     try:
        #         self.port = 12345  # Port that it uses
        #         self.server.settimeout(10)
        #         self.server.connect((self.host, self.port))
        #         break
        #     except (socket.gaierror, socket.timeout) as e:
        #         print("Invalid address try again.")
        #         ipAddress = input("Server IP Address: ")

    def login_user(self):
        user = input("Username: ")
        return user

    def login_password(self, salt):
        pw = getpass.getpass()
        hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
        return hashed_password

    def sendMessage(self, message):
        self.server.send(bytes(message, 'utf-8'))

    def recvMessage(self):
        return self.server.recv(1024).decode('utf-8')

    def sendFile(self, fileName, fileStream):
        fstream = open(fileName, 'rb')
        sent = fstream.read(int(fileStream))
        while(sent):
            self.server.send(sent)
            sent = fstream.read(int(fileStream))

# Change using byte.hex() run to mime encoding then ascii to file the output at server.
    def sendAFile(self, fileName, fileStream):
        fstream = open(fileName, 'rb')
        sent = fstream.read(int(fileStream))
        while(sent):
            self.server.send(sent)
            sent = fstream.read(int(fileStream))

    def getMD5Key(self, fileName):
        return md5ToHex(md5(fileName))

    def xorCipherString(self, string):
        return xorString(string, "key.txt")

    def xorFile(self, fileName):
        encodeDecodeFile(fileName, "xor" + fileName, "key.txt")

    def asciiArmor(self, fileName):
        file_to_ascii(fileName)

    def clientClose(self):
        self.server.close  # Close connection

    def main(self):
        while True:
            user_token = self.login_user()
            # send username to check if it exists
            self.sendMessage(user_token)

            # receive password salt for that username
            salt = (self.recvMessage()).strip()

            if salt != "0":
                pw_token = self.login_password(salt)

                # send hashed pw to authenticate
                self.sendMessage(pw_token)
                print("attempting to login...")

                # recieve confirmation of successful login
            else:
                accept = "0"

            accept = self.recvMessage().strip()

            tries = 3
            if accept == "1":

                print(self.recvMessage())

                while(tries != 0):

                    while(True):
                        try:
                            fileName = input("File: ")
                            fileStream = input("Packet Length: ")

                            print("Applying MD5...")
                            md5 = self.getMD5Key(fileName)
                            print(md5)
                            md5 = self.xorCipherString(md5)
                            print("Finished.")

                            break

                        except FileNotFoundError:
                            print("File was not found when hashing. Try again.")
                        except ValueError:
                            print("Invalid value for packet length size. Try again.")

                    print("Finished!")
                    print("XOR Cipher on file...")
                    self.xorFile(fileName)
                    print("Finished!")

                    failure = input(
                        "Would you like failure to occur?  (Y | N)").strip()

                    if(failure == "Y" or failure == "y"):
                        self.sendMessage("1")
                    else:
                        self.sendMessage("0")

                    time.sleep(1)

                    self.sendMessage(md5)

                    asciiArmor = input(
                        "Would you like to ASCII Armor? (Y | N)")

                    # ASCII Armor the chunks instead of file
                    if(asciiArmor == "Y" or asciiArmor == "y"):
                        print("Applying ASCII armoring...")
                        self.asciiArmor("xor" + fileName)
                        self.sendMessage("1")
                        print("Applied armoring.")
                        print("Sending file.")
                        self.sendFile("ascii_armored.txt", int(fileStream))
                        print("Sent.")
                    else:
                        self.sendMessage("0")
                        print("Sending file.")
                        self.sendFile("xor" + fileName, int(fileStream))
                        print("Sent.")

                    while(True):
                        self.server.settimeout(5)
                        try:
                            success = self.recvMessage().strip()
                            break
                        except socket.timeout:
                            print("Waiting for server response...")

                    if(success == "1"):
                        print("Successful transfer.")
                        break
                    else:
                        print("Transfer failure.")
                        tries -= 1
                break
            elif accept == "-1":
                print(self.recvMessage())
                break
            else:
                print(self.recvMessage())
                # Sends message back to client
                print("Invalid login information.")

        self.server.settimeout(10)
        while(True):
            self.server.settimeout(5)
            try:
                print(self.recvMessage())
                self.sendMessage("Client closing connections.")
                break
            except socket.timeout:
                print("Waiting for response.")

        self.clientClose()
