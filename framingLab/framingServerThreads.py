#! /usr/bin/env python3

import os, re, socket, sys
from threads import *
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
    s.listen(5) # Allow up to 5 connections

    while 1:
        conn, addr = s.accept()   # Accept incoming request

        worker = Worker(conn, addr)
        worker.start()

runServer()
