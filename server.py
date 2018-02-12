#!/usr/bin/env python

import socket

def checkAuthen(token):
    fileName = "users.txt"
    file = open(fileName, "r")

    with open (fileName) as f:
        for line in f.readlines():
            if(token.strip() == line.strip()):
                print ("Authorized user.")
                return True
            else:
                print ("Invalid username or password.")
                return False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start socket protocols
host = socket.gethostname() #Obtain host name
port = 12345 #Port that it uses
server.bind((host,port)) #binds a socket to address

server.listen(5) #Listen for 5 connections

(client, addr) = server.accept()  #accept connection in the bound socket
print ("Got connection from ", addr)
token = (client.recv(1024).decode('utf-8')) #Recv from connected client

print ("Checking authorization.")

if(checkAuthen(token)):
    while True:
        client.send(bytes("Thank you for connecting.",'utf-8')) #Sends message back to client
        print (client.recv(1024).decode('utf-8'))
        client.close() #Close connection with client
        break
else:
    client.send(bytes("Invalid login information.",'utf-8')) #Sends message back to client

server.close() #Close server
