#!/usr/bin/env python

from naoqi import ALProxy
import sys
import zmq
import threading
import time

class NaoCoordination(threading.Thread):
    speed = 1.0
    def __init__(self, bridge = 'tcp://localhost:8081', naohost = "cappy.dhcp", naoport = 9559):
        super(NaoCoordination, self).__init__()
        self.setDaemon(True)
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REP)
        self.sock.connect(bridge)
        self.tts = ALProxy("ALTextToSpeech", naohost, naoport)
        self.move = ALProxy("ALMotion", naohost, naoport)
        self.move.setStiffnesses("Body", 1.0)
        self.posture = ALProxy("ALRobotPosture", naohost, naoport)
        self.api = {
            'forward': self.forward,
            'backward': self.backward,
            'left': self.left,
            'right': self.right,
            'stop': self.stopMove
        }

    def run(self):
        self.move.moveInit()
        while True:
            message = self.sock.recv()
            call = self.api[message]
            self.sock.send(call())

    def left(self):
        #x, y, theta = getRobotPosition(True)
        return self.move.move(0.0, self.speed, 0.0)

    def right(self):
        return self.move.move(0.0, -self.speed, 0.0)

    def forward(self):
        return self.move.move(self.speed, 0.0, 0.0)

    def backward(self):
        return self.move.move(-self.speed, 0.0, 0.0)

    def stopMove(self):
        return self.move.stopMove()

if __name__ == "__main__":
    coord = NaoCoordination()
    print("starting")
    coord.start()
    while True:
        time.sleep(10)
