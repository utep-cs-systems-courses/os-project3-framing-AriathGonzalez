import socket, sys, re

class FramingSocket:
    contentSize = 0
    nameSize = 0
    currContent = ""  # Member this used to be msg...
    currName = ""   #
    nameList = []
    contentList = []
    extractContent = False
    
    def __init__(self, socket):
        self.socket = socket

    def frameWriter(self, compressedFile):
        bytesSent = self.socket.send(compressedFile)
        compressedFile = compressedFile[bytesSent:]

    def frameReader(self):
        while 1:
            data = self.socket.recv(1024).decode()
            if len(data) == 2:
                self.updateLists()
                self.resetData()
                break

            while len(data):
                # Get the file size.
                if self.nameSize == 0 and not self.extractContent:
                    try:
                        self.nameSize = int(data[:3])
                        data = data[3:]
                    except:
                        print("Not an int!")

                # Get content size.
                if self.extractContent:
                    try:
                        self.contentSize = int(data[:8])
                        data = data[8:]
                    except:
                        print("Not an int!")

                dataLen = len(data)
                # Two modes: Get file and Get content!
                if self.nameSize > 0:
                    data = self.getFile(dataLen, data)
                elif self.contentSize > 0:
                    data = self.getContent(dataLen, data)

            if (self.nameSize == 0 and self.contentSize == 0 and not self.extractContent):
                break

    def getFile(self, dataLen, data):
        # Can get full file in this iteration.
        if dataLen >= self.nameSize:
            fileName = data[0:self.nameSize]
            data = data[self.nameSize:]
            self.currName = self.currName + fileName
            self.nameSize = 0
            self.nameList.append(self.currName)
            self.currName = ""
            self.extractContent = True  # Fully got file -> Time to get content!
        # Can only get a portion of file in this iteration.
        elif dataLen < self.nameSize:
            fileName = data[0:dataLen]
            data = data[dataLen:]
            self.nameSize = self.nameSize - dataLen
            self.currName = self.currName + fileName
        return data

    def getContent(self, dataLen, data):
        if dataLen >= self.contentSize:
            content = data[0:self.contentSize]
            data = data[self.contentSize:]
            self.currContent = self.currContent + content
            self.contentSize = 0
            self.contentList.append(self.currContent)
            self.currContent = ""
            self.extractContent = False
        elif dataLen < self.contentSize:
            content = data[0:dataLen]
            data = data[dataLen:]
            self.contentSize = self.contentSize - dataLen
            self.currContent = self.currContent + content
        return data
    def updateLists(self):
        self.nameList.append(self.currName)
        self.contentList.append(self.currContent)
    def resetData(self):
        self.currName = ""
        self.currContent = ""
            
