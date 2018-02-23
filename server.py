#!/usr/bin/env python

import socket
import getpass
import hashlib
import crypt
import time


class Server:

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

    def recvData(self):
        with open('received_file', 'wb') as f:
            print("Opened file.")
            while True:
                print('Receiving data...')
                data = client.recv(1024)
                print('data=%s', (data))
                if not data:
                    break
                    # write data to a file
                f.write(data)
        f.close()

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
                while True:
                    # Sends message back to client
                    client.send(bytes("1", 'utf-8'))
                    # had to wait before sending next message
                    # if not, both messages read together
                    time.sleep(0.25)
                    client.send(bytes("Thank you for connecting.", 'utf-8'))

                    with open('received_file', 'wb') as f:
                        print("Opened file.")
                        while True:
                            print('Receiving data...')
                            data = client.recv(1024)
                            print('data=%s', (data))
                            if not data:
                                break
                                # write data to a file
                            f.write(data)
                    f.close()
                    break
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
        client.send(bytes(" Closing connections.", 'utf-8'))
        self.serverClose()
