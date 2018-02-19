#!/usr/bin/env python

import socket
import getpass


def login():
    user = input("Username: ")
    pw = getpass.getpass()
    token = user + "/" + pw
    return token


# Start socket protocols
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()  # Obtain host name
port = 12345  # Port that it uses


server.settimeout(10)
# Connection with host and port eg. 123.00.000.00:12345
server.connect((host, port))

while True:
    token = login()
    server.send(bytes(token, 'utf-8'))  # sends login token user/pass

    # recieve confirmation of successful login
    accept = (server.recv(1024).decode('utf-8')).strip()

    if accept == "1":
        # Print recieved from server up to 1024 bytes
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
