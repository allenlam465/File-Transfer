#!/usr/bin/env python

import socket
import getpass
import hashlib


class Client:

    server = None
    host = None
    port = None

    def __init__(self):  # creates the class object.
        pass

    def startSocket(self):
        # Start socket protocols
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()  # Obtain host name
        self.port = 12345  # Port that it uses

        self.server.settimeout(10)
        # Connection with host and port eg. 123.00.000.00:12345
        self.server.connect((self.host, self.port))

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
        sent = fstream.read(fileStream)
        while(sent):
            self.server.send(sent)
            print('Sent ', repr(sent))
            sent = fstream.read(fileStream)

    def clientClose(self):
        self.server.send(bytes("Sender closing connection.", 'utf-8'))
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

            if accept == "1":
                # Print received from server up to 1024 bytes
                print(self.recvMessage())

                fileName = input("File: ")
                fileStream = int(input("Packet Length: "))
                self.sendFile(fileName, fileStream)
                break
            elif accept == "-1":
                print(self.recvMessage())
                break
            else:
                print(self.recvMessage())
                # Sends message back to client
                print("Invalid login information.")

        self.clientClose()
