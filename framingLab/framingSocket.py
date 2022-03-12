import socket, sys, re

# Send nameLen, fileName, and fileContent to server 
def frameWriter(socket, nameLen, fileName, fileContent):
    socket.send(nameLen)
    while (len(fileName)):
        bytesSent = socket.send(fileName)
        fileName = fileName[bytesSent:]

    while (len(fileContent)):
        bytesSent = socket.send(fileContent)
        fileContent = fileContent[bytesSent:]

# Receive nameLen, fileName, and fileContent from Client
def frameReader(conn):
    data = conn.recv(1024).decode()

    if len(data) == 0:
        print ("Nothing read, terminating...")
        conn.send("0".encode())
        
    # Get Length
    nameLen = int(data[0])
    data = data[1:]

    # Get File Name
    fileName = data[0: nameLen]
    data = data [nameLen:]
    
    # Get File Contents
    fileContent = data

    return fileName, fileContent
    
    #print ("Received '%s'" % (data))
    
    #conn.shutdown(socket.SHUT_RD)   # No more input
