#!/usr/bin/env python

import getpass
import hashlib
import crypt

# login stored as user/salt/hashed_password


def create_acc():
    user = input("Input new user: ")
    pw = getpass.getpass()
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    hashed_password = hashlib.sha512((pw + salt).encode()).hexdigest()
    token = user + "/" + salt + "/" + hashed_password

    with open("users.txt", "a") as myFile:
        myFile.write(token)
        myFile.write("\n")


create_acc()
