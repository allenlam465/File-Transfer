#!/usr/bin/env python

from client import Client
from server import Server
import getpass
import crypt
import hashlib


def client():
    print("Starting client....")
    client = Client()
    ipAddress = input("Server IP Address:")
    client.startSocket(ipAddress)
    client.startSocket()
    client.main()


def server():
    print("Starting server....")
    server = Server()
    server.startSocket()
    server.main()


def create_acc():
    user = input("Input new user: ")
    pw = getpass.getpass()
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
    token = user + "/" + salt + "/" + hashed_password

    with open("users.txt", "a") as myFile:
        myFile.write(token)
        myFile.write("\n")


options = {
    '1': client,
    '2': server,
    '3': create_acc,
}

choice = input(
    "Choose from menu: \n1. Client\n2. Server\n3. Create Account\nChoice : ")
options[choice]()
