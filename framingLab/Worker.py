#! /usr/bin/env python3

import sys, threading

class Worker(threading.Thread):
    total = 0
    def __init__(self):
        threading.Thread.__init__(self)
        Worker.total += 1
        
    #def run(self):
        #global limit, total
        #for i in range(limmit):
            #total += 1
    def check(self, name):
        transferLock.acquire()
        if name in activeTransfers:
            success = false
        else:
            activeTransfers.add(name)
            success = true
        transferLock.release()
        return success
    
            
workers = [Worker() for discard in range(2)]   # Create workers

for w in workers: w.start()   # Start Workers

for w in workers: w.join()   # Wait for workers to terminate

print(total)
