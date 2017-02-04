#!/usr/bin/env python
import sys
import zmq
context = zmq.Context()

portAWS = 8082
portCoord = 8081

sockAWS = context.socket(zmq.REQ)
sockAWS.bind('tcp://*:' + str(portAWS))
sockCoord = context.socket(zmq.REQ)
sockCoord.bind('tcp://*:' + str(portCoord))
while True:
    command = sockAWS.recv()
    print 'received command "' + str(command) + '"'
    sockCoord.send(command)
    print "returned: " + str(sockCoord.recv())
