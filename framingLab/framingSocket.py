import socket, sys, re

class FramingSocket:
    size = 0
    msg = ""
    contentList = []
    
    def __init__(self, socket):
        self.socket = socket

    def frameWriter(self, compressedFile):
        bytesSent = self.socket.send(compressedFile)
        compressedFile = compressedFile[bytesSent:]

    def frameReader(self):
        while 1:
            data = self.socket.recv(1024).decode()
            if len(data) == 2:
                self.contentList.append(self.msg)
                self.msg = ""
                break

            while len(data):
                if self.size == 0:
                    try:
                        self.size = int(data[:8])
                        data = data[8:]
                    except:
                        print("Not an integer!")
                
                dataLen = len(data)
                if dataLen >= self.size:
                    content = data[0:self.size]
                    data = data[self.size:]
                    self.msg = self.msg + content
                    self.size = self.size - self.size
                    self.contentList.append(self.msg)
                    self.msg = ""
                elif dataLen < self.size:
                    content = data[0:dataLen]
                    data = data[dataLen:]
                    self.size = self.size - dataLen
                    self.msg = self.msg + content
            if (self.size == 0): break
            
            
