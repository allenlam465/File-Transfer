#!/usr/bin/env python

from client import Client
from server import Server


def client():
    print("Starting client....")
    client = Client()
    client.startSocket()
    client.main()


def server():
    print("Starting server....")
    server = Server()
    server.startSocket()
    server.main()


options = {
    '1': client,
    '2': server,
}

choice = input("Choose from menu: \n1. Client\n2. Server\nChoice : ")
options[choice]()
