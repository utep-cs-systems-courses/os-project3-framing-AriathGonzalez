#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

def archiver(fileList):
    compressedFile = []
    for fileName in fileList:
        # If file exists, add to compression
        path = "files/" + fileName
        if os.path.exists(path):
            # Open and read file
            name = fileName.encode()
            nameSize = str(len(name))
            inFile = open(path, "rb")
            content = inFile.read()
            contentSize = str(len(content))
            inFile.close()
            compressedFile.append(nameSize.encode() + name + contentSize.encode() + content)
            
    return compressedFile

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
        
        # Receive files from user
        files = input().strip()

        fileList = files.split()
        compressedFile = archiver(fileList)

        frameWriter(s, compressedFile)
client()              
