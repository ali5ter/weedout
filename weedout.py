#!/usr/bin/env python
# @file weedout.py
# Loop to detect switch state on GPIO and play randomly selected audo file
# Script to support Wen-Hao Tien's art installation, Weed Out.
# @author Alister Lewis-Bowen <alister@lewis-bowen.org>

from __future__ import print_function

import os
from os import listdir
from os import getenv
import datetime
import random
import subprocess
from time import sleep

# Check the OS so we can test outside of a RPi
if os.uname()[1] == 'raspberrypi':
    WO_RUUNING_ON_PI = True
else:
    WO_RUUNING_ON_PI = False

if WO_RUUNING_ON_PI:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  ## Use GPIO numbering not pin numbers
    GPIO.setup(23, GPIO.IN) ## Enable GPIO pin 23 as a regular input

# The directory location of the audio files
WO_AUDIO_DIR = getenv("WO_AUDIO_DIR") or './audio'
# The type of audio file to play
WO_AUDIO_TYPE = getenv("WO_AUDIO_TYPE") or 'm4a'
# How often to check for input state of GPIO pin
WO_CYCLE_TIME = getenv("WO_CYCLE_TIME") or 0.1
# Play single audio file at a time
WO_SINGLE_PLAY = getenv("WO_SINGLE_PLAY") or False
# GPIO pin number to check the input state of
WO_GPIO_PIN = 23


def get_all_audio_filenames():
    ''' Retrieve a list of all audio files found in the audio file store '''
    return [ f for f in listdir(WO_AUDIO_DIR) if f[-4:] == '.'+ WO_AUDIO_TYPE ]


def get_audio_filename():
    ''' Randomly select audio file from audio file store '''
    audiofiles = get_all_audio_filenames()
    if not audiofiles:
        return False
    return random.choice(get_all_audio_filenames())


def log_input_state():
    ''' Print log of input state '''
    print('{:%Y-%m-%d %H:%M:%S} | '.format(datetime.datetime.now()), end='')
    print('Button pressed. ', end='')


def play_random_audio_file():
    ''' Play an audio file randomly selected from file store'''
    audiofile = get_audio_filename()
    if not audiofile:
        print('Unable to select audio file to play.')
        return False
    print("Playing audio file "+ audiofile)
    if WO_RUUNING_ON_PI:
        if WO_SINGLE_PLAY:
            subprocess.call(['killall', 'cvlc'])
        os.system('cvlc '+ WO_AUDIO_DIR +'/'+ audiofile +'&')
    else:
        if WO_SINGLE_PLAY:
            subprocess.call(['killall', 'afplay'])
        os.system('afplay '+ WO_AUDIO_DIR +'/'+ audiofile +'&')


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

            if GPIO.input(WO_GPIO_PIN) == False:
                log_input_state()
                play_random_audio_file()

        else:   ## simulate change in GPIO pin state
            if random.randint(0, 100) == 42:
                log_input_state()
                play_random_audio_file()

        sleep(WO_CYCLE_TIME)

except KeyboardInterrupt:
    print("\nStopping")
    if WO_RUUNING_ON_PI:
        GPIO.cleanup()
