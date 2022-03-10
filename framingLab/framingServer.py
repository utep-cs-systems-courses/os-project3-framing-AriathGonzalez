#! /usr/bin/env python3

import os, re, socket, sys
from framingSocket import *
sys.path.append("../lib")
import params

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

                  # Receive files from client -> Try Except

                  # Save files to Database
                  path = os.path.abspath("database") + '/' + fileName

                  # Create file
                  if not os.path.exists(path):
                        os.makedirs(path)

                  # Write to file
                  with open(path, "wb") as outFile:
                        outFile.write(fileContent)
                        
                  #data = conn.recv(1024).decode() # Receive data from socket

                  #if len(data) == 0:
                       # print ("Zero length read, nothing to send, terminating")
                        #break


                  #sendMsg = ("Echoing %s" % data).encode()
                  #print ("Received '%s', sending '%s'" % (data, sendMsg.decode()))

                  #while len(sendMsg):
                       # bytesSent = conn.send(sendMsg)  # Returns the number of bytes sent
                        #sendMsg = sendMsg[bytesSent:0]

                  #conn.shutdown(socket.SHUT_WR) # Im not going to send anymore, but I'll still listen
                  #conn.close() # Disconnect socket

runServer()
