#!/usr/bin/env python

#import naoqi
import sys

from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "cappy.dhcp", 9559)
tts.setLanguage("German")
tts.say(' '.join(sys.argv[1:]))
