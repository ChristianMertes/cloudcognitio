#!/usr/bin/env python
import sys
import zmq
context = zmq.Context()

sock = context.socket(zmq.REQ)
#sock.connect(sys.argv[1])
sock.bind(sys.argv[1])
sock.send(' '.join(sys.argv[2:]))
print sock.recv()
