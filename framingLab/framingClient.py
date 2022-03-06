#! /usr/bin/env python3

import socket, sys, re
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

    outMessage = "Hello world!".encode()
    while len(outMessage):
        print("sending '%s'" % outMessage.decode())
        bytesSent = s.send(outMessage)
        outMessage = outMessage[bytesSent:]

    data = s.recv(1024).decode()
    print("Received '%s'" % data)

    s.shutdown(socket.SHUT_WR)   # No more output

    while 1:
        data = s.recv(1024).decode()
        print("Received '%s'" % data)
        if len(data) == 0:
            break
    print("Zero length read. Closing")
    s.close()

client()              
