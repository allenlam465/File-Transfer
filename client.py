#!/usr/bin/env python

import socket
import getpass
import hashlib


def login_user():
    user = input("Username: ")
    return user


def login_password(salt):
    pw = getpass.getpass()
    hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
    return hashed_password


# Start socket protocols
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()  # Obtain host name
port = 12345  # Port that it uses


server.settimeout(10)
# Connection with host and port eg. 123.00.000.00:12345
server.connect((host, port))

while True:
    user_token = login_user()
    # send username to check if it exists
    server.send(bytes(user_token, 'utf-8'))

    # receive password salt for that username
    salt = (server.recv(1024).decode('utf-8')).strip()

    print(salt)

    if salt != "0":
        pw_token = login_password(salt)

        # send hashed pw to authenticate
        server.send(bytes(pw_token, 'utf-8'))
        print("attempting to login...")

        # recieve confirmation of successful login
        accept = (server.recv(1024).decode('utf-8')).strip()
    else:
        accept = "0"

    if accept == "1":
        # Print received from server up to 1024 bytes
        print(server.recv(1024).decode('utf-8'))

        fileName = input("File: ")

        fstream = open(fileName, 'rb')
        sent = fstream.read(1024)
        while(sent):
            server.send(sent)
            print('Sent ', repr(sent))
            sent = fstream.read(1024)
        break
    elif accept == "-1":
        print(server.recv(1024).decode('utf-8'))
        break
    else:
        print(server.recv(1024).decode('utf-8'))
        print("Invalid login information.")  # Sends message back to client

server.send(bytes("Sender closing connection.", 'utf-8'))
server.close  # Close connection

