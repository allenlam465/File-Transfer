#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start socket protocols
host = socket.gethostname() #Obtain host name
port = 12345 #Port that it uses
s.bind((host,port)) #binds a socket to address

s.listen(5) #Listen for 5 connections

while True:
    (c, addr) = s.accept()  #accept connection in the bound socket
    print "Got connection from ", addr
    c.send("Thank you for connecting.") #Sends message back to client
    c.close() #Close connection with client
    break

s.close() #Close server
