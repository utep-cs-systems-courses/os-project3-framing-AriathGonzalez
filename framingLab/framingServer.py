#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

def saveToDB(fileName, fileContent):
      path = "database/" + fileName
                  
      # Create file if it doesnt exist
      if not os.path.exists(path):
            print (os.getcwd())
            os.chdir("database")
            #os.makedirs(fileName)
            print (os.getcwd())
            open(fileName, 'x')

      # Write to file
      with open(fileName, "w") as outFile:
            outFile.write(fileContent)
                  
def runServer():
      switchesVarDefaults = (
          (('-l', "--listenPort"), "listenPort", 50001),
      ) 

      paramMap = params.parseParams(switchesVarDefaults)

      listenPort = paramMap["listenPort"]
      listenAddr = ''  # Symbolic name meaning all available interfaces

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket to listen
      s.bind((listenAddr, listenPort))  # Bind socket to address (Ready to listen at a loc)
      s.listen(2) # Allow up to 2 connections
      
      # Returns pair (conn, addr)
      # conn is a new socket to send and receive data on the connection
      # addr is the addr bound to the socket on the other end of the connection (connected by)

      while 1:
            conn, addr = s.accept()   # Accept incoming request
            
            if os.fork() == 0:   # Child becomes server
                  fileName, fileContent = frameReader(conn)
                  print ("Back in Server...")

                  # Receive files from client -> Try Except

                  # Save files to Database
                  saveToDB(fileName, fileContent)
                        
                  #conn.shutdown(socket.SHUT_WR) # Im not going to send anymore, but I'll still listen
                  #conn.close() # Disconnect socket

runServer()
