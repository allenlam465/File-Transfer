#!/usr/bin/env python

import socket
import getpass

def login():
    user = input("Username: ")
    pw = getpass.getpass()
    token = user + "/" + pw
    return token

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start socket protocols
host = socket.gethostname() #Obtain host name
port = 12345 #Port that it uses

while True:
    token = login()
    server.connect((host, port)) #Connection with host and port eg. 123.00.000.00:12345
    server.send(bytes(token, 'utf-8'))
    print (server.recv(1024).decode('utf-8')) #Print recieved from server up to 1024 bytes

server.send(bytes("Sender closing connection.", 'utf-8'))
server.close #Close connection
