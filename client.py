#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start socket protocols
host = socket.gethostname() #Obtain host name
port = 12345 #Port that it uses

s.connect((host, port)) #Connection with host and port eg. 123.00.000.00:12345
print s.recv(1024) #Print recieved from server up to 1024 bytes
s.close #Close connection
