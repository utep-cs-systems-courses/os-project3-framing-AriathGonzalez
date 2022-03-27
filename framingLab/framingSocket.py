import socket, sys, re

# Send compressed file to Server
def frameWriter(socket, compressedFile):
    while len(compressedFile):
        bytesSent = socket.send(compressedFile)
        compressedFile = compressedFile[bytesSent:]
    
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
        nameSize = int(data[:firstChar(data)])
        data = data[firstChar(data):]
        
        name = data[0:nameSize]
        data = data[nameSize:]
        
        # Get Content
        contentSize = int(data[:firstChar(data)])
        data = data[firstChar(data):]

        content = data[0:contentSize]
        data = data[contentSize:]

        # Append to lists
        nameList.append(name)
        contentList.append(content)
    return (nameList, contentList)
    
# Finds position of first character, to get the size of files
def firstChar(data):
    for i in range(len(data)):
        if data[i].isalpha():
            return i
    return -1
                       
                       
