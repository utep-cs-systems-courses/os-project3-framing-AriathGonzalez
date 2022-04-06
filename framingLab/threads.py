#! /usr/bin/env python3

import itertools, os, sys, threading
from framingSocket import *

class Worker(threading.Thread):
    activeFiles = set()
    transferLock = threading.Lock()
    total = 0
    
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        Worker.total += 1
        self.conn = conn
        self.addr = addr
        
    def check(self, name):
        self.transferLock.acquire()   # Lock
        if name in self.activeFiles:
            success = False
        else:
            self.activeFiles.add(name)
            success = True
        self.transferLock.release()
        return success
    
    def run(self):
        contentList = frameReader(self.conn)
        directory = os.getcwd()
        
        for content in contentList:
            fileCount = len(os.listdir(directory))
            fileName = "file" + str(fileCount + 1) + ".txt"
            canSave = self.check(fileName)

            if (canSave):
                open(fileName, 'x')

                # Write to file
                with open(fileName, 'w') as outFile:
                    outFile.write(content)
                
            else:
                print ("File is in active")
                self.conn.send("0".encode())   # Unsuccessful

            self.activeFiles.remove(fileName)
        self.conn.send("1".encode())   # Successful
