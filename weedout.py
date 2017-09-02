#!/usr/bin/env python
# @file weedout.py
# Loop to detect switch state on GPIO and play randomly selected audo file
# Script to support Wen-Hao Tien's art installation, Weed Out.
# @author Alister Lewis-Bowen <alister@lewis-bowen.org>

# Requirements:
#
# * Wen moves m4a files from her iphone to RPi
# * To play m4a audio files:
#     sudo apt-get install vlc-nox
#     cvlc /pat/to/your/file.m4a
#

from __future__ import print_function

import os
from time import sleep
import random
import RPi.GPIO as GPIO

# Hardware configuration:
#
#  3.3v -------.
#              |
#             [ ] 10K pull up resistor
#              |
#              |---------- GPIO input pin
#              |
#               \ push switch
#              |
#  GND --------'
#
# Pull up resistor used to make sure GPIO input pin is either 0v when pressed
# or GND when 3.3v when open. When GPIO pin is set up as an Input, we check if
# False (or GPIO.LOW) to detect if push switch pressed.
#
GPIO.setmode(GPIO.BCM)  ## Use GPIO numbering not pin numbers
GPIO.setup(23, GPIO.IN) ## Enable GPIO pin 23 as a regular input

WO_AUDIO_DIR = '~/weedo/audio'
WO_CYCLE_TIME = 0.1     ## How often to check for input state of GPIO pin

_DEBUG = False


def getAudioFileNames()
    ''' Retrieve a list of all audio files found in the audio file store '''
    files = [ f for f in listdir('.') if f[-4:] == '.m4a' ]
    if not (len(mp3_files) > 0):
        print("No audio files found in "+ WO_AUDIO_DIR)
    return files


def getAudioFileName()
    ''' Randomly select audio file from audio file store '''
    file = random.choice(getAudioFileNames())
    if file:
        print("Selected audio file: "+ file)
        return file
    else:
        return false


# Loop to check for state of GPIO pin

print(" /$$      /$$                           /$$        /$$$$$$              /$$    ")
print("| $$  /$ | $$                          | $$       /$$__  $$            | $$    ")
print("| $$ /$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  \ $$ /$$   /$$ /$$$$$$  ")
print("| $$/$$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$  | $$| $$  | $$|_  $$_/  ")
print("| $$$$_  $$$$| $$$$$$$$| $$$$$$$$| $$  | $$      | $$  | $$| $$  | $$  | $$    ")
print("| $$$/ \  $$$| $$_____/| $$_____/| $$  | $$      | $$  | $$| $$  | $$  | $$ /$$")
print("| $$/   \  $$|  $$$$$$$|  $$$$$$$|  $$$$$$$      |  $$$$$$/|  $$$$$$/  |  $$$$/")
print("|__/     \__/ \_______/ \_______/ \_______/       \______/  \______/    \___/  ")
print("\nFound the following audio files to work with...")
print(getAudioFileNames())
print("\nListening...")

try:
    while True:
    if (GPIO.input(23) == False):
        print("Button pressed")
        subprocess.call(['killall', 'cvlc'])    ## stop any playing audio
        os.system('cvlc '+ WO_AUDIO_DIR +'/'+ getAudioFileName() +'&')  ## play audio

    sleep(WO_CYCLE_TIME)

except KeyboardInterrupt:
    print("\nStopping")
    GPIO.cleanup()
