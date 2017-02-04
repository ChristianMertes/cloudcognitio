#!/usr/bin/env python
import sys
import zmq
import time
context = zmq.Context()

portAWS = 8082
portCoord = 8081

sockAWS = context.socket(zmq.REQ)
sockAWS.bind('tcp://*:' + str(portAWS))
sockCoord = context.socket(zmq.REQ)
sockCoord.bind('tcp://*:' + str(portCoord))
command = None
relayed = True
while True:
    try:
        if relayed:
            command = sockAWS.recv()
            print 'received command "' + str(command) + '"'
            sockCoord.send(command)
        response = sockCoord.recv()
        print "returned: " + str(response)
        sockAWS.send(response)
    except Exception as e:
        print e
        time.sleep(.1)

