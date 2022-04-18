#! /usr/bin/env python3

import os, sys, threading
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
        fr = FramingSocket(self.conn)
        fr.frameReader()
        nameList = fr.nameList
        contentList = fr.contentList
        directory = os.getcwd()

        for (name, content) in zip(nameList, contentList):
            canSave = self.check(name)
            if (canSave):
                path = "database/" + name

                # Create file if it doesnt exist
                if not os.path.exists(path):
                    open(name, 'x')

                    # Write to file
                    with open(name, 'w') as outFile:
                        outFile.write(content)
                elif os.path.exists(path):
                    print("File already exists in database")
            # If two files in transfer, change the name of the second file.
            else:
                print("File is in active transfer.")
                pos = name.index('.')
                num = int(name[pos - 1])   # Get position of number in file.
                newName = "file" + str(num + 1) + ".txt"

                # Create file
                open(newName, 'x')

                with open(newName, 'w') as outFile:
                    outFile.write(content)
        self.conn.send("1".encode())  # Successful
