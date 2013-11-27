#!/usr/bin/env python2
# -*- coding: utf8 -*-

# TODO :
# stty -hup -F /dev/ttyUSB0

import serial
import time
import math
import sys

if(len(sys.argv) < 2):
	sys.exit("Usage : ./test_serial.py PORT")

try:
	ser = serial.Serial(sys.argv[1], 115200)
except:
	sys.exit("Erreur à l'ouverture du port série.")

for i in range(1, 127):
	for j in [0x80, 0, 0, i]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

ser.close()
