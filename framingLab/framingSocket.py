import socket, sys, re

# Send nameLen, fileName, and fileContent to server 
def frameWriter(socket, nameLen, fileName, fileContent):
    print ("In frameWriter...")
    socket.send(nameLen)
    while (len(fileName)):
        bytesSent = socket.send(fileName)
        fileName = fileName[bytesSent:]

    while (len(fileContent)):
        bytesSent = socket.send(fileContent)
        fileContent = fileContent[bytesSent:]

# Receive nameLen, fileName, and fileContent from Client
def frameReader(conn):
    print ("In frameReader...")
    data = conn.recv(1024).decode()

    if len(data) == 0:
        print ("Nothing read, terminating...")
        sys.exit(1)
        
    # Get Length
    nameLen = int(data[0])
    data = data[1:]

    # Get File Name
    fileName = data[0: nameLen]
    data = data [nameLen:]
    
    # Get File Contents
    fileContent = data

    # Send Status Code - Success

    return fileName, fileContent
    
    #print ("Received '%s'" % (data))

    # Send Status Code 1 - Success, 0 - Fail

    #conn.shutdown(socket.SHUT_RD)   # No more input
