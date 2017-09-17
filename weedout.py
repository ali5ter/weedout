#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Weed Out: RPi script to support Wen-Hao Tien's art installation

Loop to detect switch state on GPIO pin and play randomly selected audo file

Author: Alister Lewis-Bowen <alister@lewis-bowen.org>
"""

from __future__ import print_function

import os
from os import listdir
from os import getenv
import datetime
import random
import subprocess
from time import sleep

# The directory location of the audio files
WO_AUDIO_DIR = getenv("WO_AUDIO_DIR") or getenv("PWD") +'/audio'
# The type of audio file to play
WO_AUDIO_TYPE = getenv("WO_AUDIO_TYPE") or 'm4a'
# How often to check for input state of GPIO pin
WO_CYCLE_TIME = getenv("WO_CYCLE_TIME") or 0.1
# Play single audio file at a time
WO_SINGLE_PLAY = getenv("WO_SINGLE_PLAY") or False
# GPIO pin number to check the input state of
WO_GPIO_PIN = 23

# Check the OS so we can test outside of a RPi
if os.uname()[1] == 'raspberrypi':
    WO_RUNNING_ON_RPI = True
else:
    WO_RUNNING_ON_RPI = False

## Enable RPi hardware
if WO_RUNNING_ON_RPI:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)              ## Use GPIO numbering not pin numbers
    GPIO.setup(WO_GPIO_PIN, GPIO.IN)    ## Enable GPIO pin as a regular input


def get_all_audio_filenames():
    ''' Retrieve a list of all audio files found in the audio file store '''
    return [ f for f in listdir(WO_AUDIO_DIR) if not f.startswith('.') if f[-4:] == '.'+ WO_AUDIO_TYPE ]


def get_audio_filename():
    ''' Randomly select audio file from audio file store '''
    audiofiles = get_all_audio_filenames()
    if not audiofiles:
        return False
    return random.choice(get_all_audio_filenames())


def log(message):
    ''' Print log of input state '''
    print('{:%Y-%m-%d %H:%M:%S} | '.format(datetime.datetime.now()), end='')
    print(message, end='')


def play_audio_file(audiofile):
    ''' Play an audio file of the given name from file store'''
    print("Playing audio file "+ audiofile)
    if WO_RUNNING_ON_RPI:
        if WO_SINGLE_PLAY:
            subprocess.call(['killall', 'cvlc'])
        os.system('cvlc '+ WO_AUDIO_DIR +'/'+ audiofile +' 2>/dev/null &')
    else:
        if WO_SINGLE_PLAY:
            subprocess.call(['killall', 'afplay'])
        os.system('afplay '+ WO_AUDIO_DIR +'/'+ audiofile +'&')


def play_random_audio_file():
    ''' Play an audio file randomly selected from file store'''
    audiofile = get_audio_filename()
    if not audiofile:
        print('Unable to select audio file to play.')
        return False
    play_audio_file(audiofile)
    

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
play_audio_file('.startup.m4a')
print("\nWaiting for input...")

# Loop to check for state of GPIO pin
try:
    _IS_PRESSED = False  ## used to detect first detection of pressed button

    while True:
        if WO_RUNNING_ON_RPI:

            if not GPIO.input(WO_GPIO_PIN):
		if not _IS_PRESSED:
                    log('Button pressed. ')
                    play_random_audio_file()
                    _IS_PRESSED = True
                else:
                    log('Button released. ')
		    print('')
                    _IS_PRESSED = False  ## button released

        else:   ## simulate change in GPIO pin state
            if random.randint(0, 100) == 42:
                log('Simlated state change. ')
                play_random_audio_file()

        sleep(WO_CYCLE_TIME)

except KeyboardInterrupt:
    print("\nStopping")
    if WO_RUNNING_ON_RPI:
        GPIO.cleanup()
