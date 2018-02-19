#!/usr/bin/env python

import socket
import getpass
import hashlib
import crypt


#login stored as user/salt/hashed_password
def createAcc():
    user = input("Input new user:")
    pw = getpass.getpass()
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
    token = user + "/" + salt + "/" + hashed_password

    with open("user.txt", "a") as myFile:
        myFile.write(token)
        myFile.write("\n")

def checkLogin(token):
    fileName = "users.txt"
    file = open(fileName, "r")
    with open(fileName) as f:
        for line in f.readlines():
            split = line.split("/")
            if token.strip() == split[0].strip():
                return split[1]  # return salt

    print("Invalid username.")
    return -1


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
    # receive username from client
    login_token = (client.recv(1024).decode('utf-8'))
    print("received login: " + login_token)

    # return salt to client
    salt = checkLogin(login_token).strip()
    if salt == -1:
        # invalid username subtract 1 try
        tries -= 1
    else:
        print("found salt, sending: " + salt)
        sendMessage(salt)
        # receive password hash from client
        pw_token = (client.recv(1024).decode('utf-8')).strip()

        # concat login/salt/pw
        token = login_token + "/" + salt + "/" + pw_token
        print(token)

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
