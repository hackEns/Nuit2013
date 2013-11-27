#!/usr/bin/env python2

# TODO :
# stty -hup -F /dev/ttyUSB0

import serial
import time
import math

ser = serial.Serial('/dev/ttyUSB1', 115200)

for i in range(1, 127):
	for j in [0x80, 0, 0, i]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

ser.close()
