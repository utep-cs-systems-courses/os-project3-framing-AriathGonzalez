import socket, sys, re

# Send compressed file to Server
def frameWriter(socket, compressedFile):
    while len(compressedFile):
        bytesSent = socket.send(compressedFile)
        compressedFile = compressedFile[bytesSent:]
    
# Decompress compressed file from Client
def frameReader(conn):
    data = conn.recv(1024).decode()
    print ("Received: ", data)
    if len(data) == 0:
        print ("Nothing read, terminating...")
        conn.send("0".encode())

    contentList = []

    while len(data):    
        # Get Content
        contentSize = int(data[:8])
        data = data[8:]
        print ("contentSize: ", contentSize)

        content = data[0:contentSize]
        data = data[contentSize:]
        print ("content: ", content)
        print ("data: ", data)

        # Append to list
        contentList.append(content)
    return contentList
