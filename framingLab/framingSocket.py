import socket, sys, re

# Send compressed file to Server
def frameWriter(socket, compressedFile):
    for singleFile in compressedFile:
        while len(singleFile):
            bytesSent = socket.send(singleFile)
            singleFile = singleFile[bytesSent:]
    
# Decompress compressed file from Client
def frameReader(conn):
    data = conn.recv(1024).decode()
    
    if len(data) == 0:
        print ("Nothing read, terminating...")
        conn.send("0".encode())

    print ("Received '%s'" % (data))
    print (type(data))

    nameList = []
    contentList = []

    while len(data):
        # Get Name
        nameSize = int(data[0])
        data = data[1:]
        
        name = data[0:nameSize]
        #print (name)
        data = data[nameSize:]
        #print(data)
        # Get Content
        contentSize = int(data[0])
        data = data[1:]

        content = data[0:contentSize]
        data = data[contentSize:]

        # Append to lists
        nameList.append(name)
        contentList.append(content)
        
    #conn.shutdown(socket.SHUT_RD)   # No more input
