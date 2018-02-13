#!/usr/bin/env python

import socket
import getpass

def login():
    user = input("Username: ")
    pw = getpass.getpass()
    token = user + "/" + pw
    return token

def ping(hostName):
    host = hostName
    response = os.system("ping -c 1" + host)

    if (response == 0):
        return True
    else:
        return False

def sendFile(fileName):
    with open(fileName, 'rb') as fstream:
        while True:
            data = fstream.read(1024)
            print ("Sending data...")
            server.send(data)
            print ("Sent data.")
            fstream.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start socket protocols
host = socket.gethostname() #Obtain host name
port = 12345 #Port that it uses

token = login()
server.connect((host, port)) #Connection with host and port eg. 123.00.000.00:12345

while ping(host):
    #print ("What is the file name?")
    #fileName = input("Filename: ")
    #sendFile(fileName)
    server.send(bytes(token, 'utf-8'))
    print (server.recv(1024).decode('utf-8')) #Print recieved from server up to 1024 bytes
    break

server.send(bytes("Sender closing connection.", 'utf-8'))
server.close #Close connection
