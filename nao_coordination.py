#!/usr/bin/env python
# -*- coding: utf-8 -*-

from naoqi import ALProxy
import sys
import zmq
import threading
import time
import random
import signal
import sys

class NaoCoordination(threading.Thread):
    speed = 1.0
    responses = ["Aber gerne", "Okay", "Alles klar"]
    filename = '/tmp/personen.txt'
    #responses = ["Aber gerne", "Okay", "Alles klar", "Mache ich"]
    def __init__(self, bridge = 'tcp://localhost:8081', naohost = "cappy.dhcp", naoport = 9559):
        super(NaoCoordination, self).__init__()
        self.setDaemon(True)
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REP)
        if bridge:
            self.sock.connect(bridge)
        else:
            self.sock.bind('tcp://*:8081')
        self.tts = ALProxy("ALTextToSpeech", naohost, naoport)
        self.move = ALProxy("ALMotion", naohost, naoport)
        self.move.setStiffnesses("Body", 1.0)
        self.posture = ALProxy("ALRobotPosture", naohost, naoport)
        self.auto = ALProxy("ALAutonomousLife", naohost, naoport)
        #ALProxy("ALAutonomousMoves", naohost, naoport).setBackgroundStrategy("none")
        #ALProxy("ALAutonomousMoves", naohost, naoport).setExpressiveListeningEnabled(False)
        #ALProxy("ALBasicAwareness", naohost, naoport).stopAwareness()
        self.api = {
            'vorwärts': self.forward,
            'rückwärts': self.backward,
            'links': self.left,
            'rechts': self.right,
            'stopp': self.stopMove,
            'stop': self.stopMove,
            'halt': self.stopMove,
            'aufstehen': self.stand,
            'hinsetzen': self.sit,
            'personen': self.faces,
        }
        self.faces = ["gesichter", "personen"]
        def signal_handler(signal, frame):
            print('Aborting...')
            #connection = ALProxy("ALConnectionManager", naohost, naoport)
            #connection.disconnect()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def faces(self):
        pass

    def run(self):
        #ALAutonomousMoves.setExpressiveListeningEnabled(False)
        #ALBasicAwareness.stopAwareness()
        #ALAutonomousMoves.setBackgroundStrategy("none")
        self.auto.stopAll()
        self.posture.goToPosture("StandInit", 0.5)
        self.move.moveInit()
        self.tts.setLanguage("German")
        while True:
            try:
                print 'listening for message'
                message = self.sock.recv()
                print 'received "' + str(message) + '"'
                #print self.api
                try:
                    call = self.api[message]
                except KeyError:
                    self.sock.send("Das habe ich leider nicht verstanden")
                    continue
                #print 'translated to call "' + str(call) + '"'
                if message in self.faces:
                    f = open(self.filename, 'r')
                    response = f.read()
                else:
                    response = random.choice(self.responses)
                print 'responding:', response
                self.sock.send(response)
                call()
                self.tts.say(random.choice(self.responses))
            except Exception as e:
                print 'caught exception:', e
                time.sleep(1)
                
    def left(self):
        #x, y, theta = getRobotPosition(True)
        return self.move.move(0.0, self.speed, 0.0)

    def right(self):
        return self.move.move(0.0, -self.speed, 0.0)

    def forward(self):
        return self.move.move(self.speed, 0.0, 0.0)

    def backward(self):
        return self.move.move(-self.speed, 0.0, 0.0)

    def sit(self):
        return self.posture.goToPosture("Sit", 0.5)

    def stand(self):
        return self.posture.goToPosture("StandInit", 0.5)

    def stopMove(self):
        return self.move.stopMove()

if __name__ == "__main__":
    coord = NaoCoordination(bridge = None)
    print("starting")
    coord.start()
    while True:
        time.sleep(10)
