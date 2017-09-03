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
from os import listdir
from os import getenv
import random
import subprocess
from time import sleep

# Check the OS so we can test outside of a RPi
if os.uname()[1] == 'raspberrypi':
    WO_RUUNING_ON_PI = True
else:
    WO_RUUNING_ON_PI = False

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
if WO_RUUNING_ON_PI:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  ## Use GPIO numbering not pin numbers
    GPIO.setup(23, GPIO.IN) ## Enable GPIO pin 23 as a regular input

# The directory location of the audio files
WO_AUDIO_DIR = getenv("WO_AUDIO_DIR") or './audio'
# How often to check for input state of GPIO pin
WO_CYCLE_TIME = getenv("WO_CYCLE_TIME") or 0.1


def get_all_audio_filenames():
    ''' Retrieve a list of all audio files found in the audio file store '''
    return [ f for f in listdir(WO_AUDIO_DIR) if f[-4:] == '.m4a' ]


def get_audio_filename():
    ''' Randomly select audio file from audio file store '''
    return random.choice(get_all_audio_filenames())


# Loop to check for state of GPIO pin

print("\n")
print(" /$$      /$$                           /$$        /$$$$$$              /$$    ")
print("| $$  /$ | $$                          | $$       /$$__  $$            | $$    ")
print("| $$ /$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  \ $$ /$$   /$$ /$$$$$$  ")
print("| $$/$$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$  | $$| $$  | $$|_  $$_/  ")
print("| $$$$_  $$$$| $$$$$$$$| $$$$$$$$| $$  | $$      | $$  | $$| $$  | $$  | $$    ")
print("| $$$/ \  $$$| $$_____/| $$_____/| $$  | $$      | $$  | $$| $$  | $$  | $$ /$$")
print("| $$/   \  $$|  $$$$$$$|  $$$$$$$|  $$$$$$$      |  $$$$$$/|  $$$$$$/  |  $$$$/")
print("|__/     \__/ \_______/ \_______/ \_______/       \______/  \______/    \___/  ")
FILES = get_all_audio_filenames()
if not FILES:
    print("\nUnable to find any audio files in: "+ WO_AUDIO_DIR)
    exit()
print("\nFound the following audio files to work with...")
print(FILES)
print("\nListening...")

try:
    while True:
        if WO_RUUNING_ON_PI:

            if GPIO.input(23) == False:
                print("Button pressed")
                subprocess.call(['killall', 'cvlc'])    ## stop any playing audio
                os.system('cvlc '+ WO_AUDIO_DIR +'/'+ get_audio_filename() +'&')  ## play audio

        else:
            if random.randint(0, 100) == 42:    ## simulate change in GPIO pin state
                ## Specifically for macOS..
                os.system('afplay '+ WO_AUDIO_DIR +'/'+ get_audio_filename() +'&')

        sleep(WO_CYCLE_TIME)

except KeyboardInterrupt:
    print("\nStopping")
    if WO_RUUNING_ON_PI:
        GPIO.cleanup()
