#!/usr/bin/env python
import sys
import zmq

context = zmq.Context()
sock = context.socket(zmq.REP)
#sock.bind(sys.argv[1])
sock.connect(sys.argv[1])

while True:
    message = sock.recv()
    sock.send('Echoing: ' + message)
