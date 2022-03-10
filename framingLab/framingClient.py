#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

def client():
    switchesVarDefaults = (
        (('-s', "--server"), "server", "127.0.0.1:50001"),
    )
      
    paramMap = params.parseParams(switchesVarDefaults)

    server = paramMap["server"]

    try:
        serverHost, serverPort = re.split(':', server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)
        
    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res

        # Try creating socket based on above info
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        # Try to connect to remote socket at given address
        try:
            print(" attempting to connect to %s" % repr(sa))
            s.connect(sa)
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
        break

    if s is None:
        print("Could not open socket")
        sys.exit(1)


    while 1:
        # Receive file from user
        fileName = input().strip()
        nameLen = str(len(fileName))

        path = "files/" + fileName
        
        # Check if file sent exists
        if os.path.exists(path):
            print ("Checking if file exists...")
            # Open and read file
            inFile = open(path, "rb")
            fileContent = inFile.read()

            # Check if empty
            if len(fileContent) == 0:
                sys.exit(1)

            # Send frames to Server
            frameWriter(s, nameLen.encode(), fileName.encode(), fileContent)
            inFile.close()

            #s.shutdown(socket.SHUT_WR)   # No more output

            # Check if successful transfer -> Receive code from server?

            #s.close()
            
        # No such file
        else:
            print ("No such file")
            sys.exit(1)
client()              
