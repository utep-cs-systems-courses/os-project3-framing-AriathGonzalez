#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

def saveToDB(socket, contentList):
      os.chdir("database")
      directory = os.getcwd()
      
      for content in contentList:
            fileCount = len(os.listdir(directory))   # Get count of fileNames in DB

            print (fileCount)

            fileName = "file" + str(fileCount + 1) + ".txt"
                  
            open(fileName, 'x')

            # Write to file
            with open(fileName, "w") as outFile:
                  outFile.write(content)
      #socket.send("1".encode())   # Success
                            
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
            fr = FramingSocket(conn)
            print('Connected by', addr)

            if os.fork() == 0:   # Child becomes server
                  fr.frameReader()
                  contentList = fr.contentList

                  print("Printing content...")
                  for content in contentList:
                        print(content)
                  # Save files to Database
                  saveToDB(conn, contentList)
runServer()
