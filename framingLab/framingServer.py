#! /usr/bin/env python3

import socket, sys, re
sys.path.append("../lib")
import params

def runServer():
      switchesVarDefaults = (
          (('-l', "--listenPort"), "listenPort", 50001),
      ) 

      paramMap = params.parseParams(switchesVarDefaults)

      listenPort = paramMap["listenPort"]
      listenAddr = ''  # Symbolic name meaning all available interfaces

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create Socket
      s.bind((listenAddr, listenPort))  # Bind socket to address (Ready to listen at a loc)
      s.listen(1) # Allow only one connection
      
      conn, addr = s.accept() # Accept incoming request
      # Returns pair (conn, addr)
      # conn is a new socket to send and receive data on the connection
      # addr is the addr bound to the socket on the other end of the connection (connected by)

      while 1:
          data = conn.recv(1024).decode() # Receive data from socket

          if len(data) == 0:
              print ("Zero length read, nothing to send, terminating")
              break


          sendMsg = ("Echoing %s" % data).encode()
          print ("Received '%s', sending '%s'" % (data, sendMsg.decode()))

          while len(sendMsg):
              bytesSent = conn.send(sendMsg)  # Returns the number of bytes sent
              sendMsg = sendMsg[bytesSent:0]

      conn.shutdown(socket.SHUT_WR) # Im not going to send anymore, but I'll still listen
      conn.close() # Disconnect socket

runServer()
