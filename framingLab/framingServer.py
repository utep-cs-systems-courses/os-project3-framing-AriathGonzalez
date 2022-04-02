#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

def saveToDB(socket, contentList):
      os.chdir("database")
      for i in range(len(contentList)):
            fileName = "file" + str(i) + ".txt"
            path = "database/" + fileName
                  
            # Create file if it doesnt exist
            if not os.path.exists(path):
                  open(fileName, 'x')

                  # Write to file
                  with open(fileName, "w") as outFile:
                        outFile.write(contentList[i])
            elif os.path.exists(path):
                  print ("File already exists in database")
      socket.send("1".encode())   # Success
                            
def runServer():
      switchesVarDefaults = (
          (('-l', "--listenPort"), "listenPort", 50001),
      ) 

      paramMap = params.parseParams(switchesVarDefaults)

      listenPort = paramMap["listenPort"]
      listenAddr = ''  # Symbolic name meaning all available interfaces

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket to listen
      s.bind((listenAddr, listenPort))  # Bind socket to address (Ready to listen at a loc)
      s.listen(5) # Allow up to 5 connections

      while 1:
            conn, addr = s.accept()   # Accept incoming request
            print('Connected by', addr)

            if os.fork() == 0:   # Child becomes server
                  contentList = frameReader(conn)
                  
                  # Save files to Database
                  saveToDB(conn, contentList)
runServer()
