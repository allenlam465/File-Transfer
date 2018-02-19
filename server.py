#!/usr/bin/env python

import socket
import getpass


def createAcc():
    user = input("Input new user:")
    pw = getpass.getpass()
    token = user + "/" + pw

    with open("user.txt", "a") as myFile:
        myFile.write(token)


def checkAuthen(token):
    fileName = "users.txt"
    file = open(fileName, "r")

    with open(fileName) as f:
        for line in f.readlines():
            if(token.strip() == line.strip()):
                print("Authorized user.")
                return True

    print("Invalid username or password.")
    return False


def sendMessage(message):
    # Sends message back to client on server
    client.send(bytes(message, 'utf-8'))


def serverClose():
    sendMessage(" Closing connections.")
    server.close()  # Close server


# Start socket protocols
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()  # Obtain host name
port = 12345  # Port that it uses
server.bind((host, port))  # binds a socket to address

server.listen(5)  # Listen for 5 connections
print("Listening for client.")

(client, addr) = server.accept()  # accept connection in the bound socket
print("Got connection from ", addr)

tries = 3

while(tries != 0):
    token = (client.recv(1024).decode('utf-8'))  # Recv from connected client

    print("Checking authorization.")

    if(checkAuthen(token)):
        while True:
            sendMessage("1")  # Sends message back to client
            sendMessage("Thank you for connecting.")

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
            sendMessage("-1")
            sendMessage("Too many tries server closing.")
            break
        else:
            sendMessage("0")
            line = "Number tries left: " + str(tries)
            sendMessage(line)

serverClose()
