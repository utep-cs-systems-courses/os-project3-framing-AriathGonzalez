#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
from lib import params

def archiver(fileList):
    byteArr = bytearray()

    for fileName in fileList:
        path = "files/" + fileName
        with open(path, "rb") as file:
            tmpByteArr = bytearray()
            tmpByteArr = file.read()
        tmpFile = f"{len(fileName):03d}".encode() + fileName.encode()
        byteArr = byteArr + tmpFile + f"{len(tmpByteArr):08d}".encode() + tmpByteArr
    return byteArr

def client():
    # Server 50001, Stammer 50000
    switchesVarDefaults = (
        (('-s', "--server"), "server", "127.0.0.1:50000"),
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
        fw = FramingSocket(s)
        fw.frameWriter(compressedFile)

        # Check if successful transfer
        status = s.recv(1024).decode()
        status = int(status)
        
        if (status):
            print ("Successful in adding new file to Database.")
            sys.exit(1)
        elif (not status):
            print ("Unsuccessful in adding new file to Database.")
            sys.exit(0)
client()
