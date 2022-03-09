import socket, sys, re

def frameWriter(socket, fileLen, fileName, fileContent):
    # Try sending fileName first, and then the filecontent
    while (len(fileName)):
        bytesSent = socket.send(fileName)
        fileName = fileName[bytesSent:]

    while (len(fileContent)):
        bytesSent = socket.send(fileContent)
        fileContent = fileContent[bytesSent:]
    #while len(data):
        #bytesSent = socket.send(data)
        #data = data[bytesSent:]

def frameReader(conn):
    data = conn.recv(1024).decode()

    # Check if len of data is 0
    if len(data) == 0:
        print ("Nothing read, terminating...")
        sys.exit(1)
        
    print ("Received '%s'" % (data))

    # Send Status Code 1 - Success, 0 - Fail

    #conn.shutdown(socket.SHUT_RD)   # No more input