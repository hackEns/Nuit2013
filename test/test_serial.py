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

k = 0
for i in range(1, 10):
	for i in range(1, 127):
		for j in [0x80, 0, 0, i]:
			k+=1
			print k
			ser.write(chr(j))
		#time.sleep(math.exp(-i/500)*0.07)
		time.sleep(0.01)

	for i in range(1, 127):
		for j in [0x81, 0, 0, i]:
			k+=1
			print k
			ser.write(chr(j))
		#time.sleep(math.exp(-i/500)*0.07)
		time.sleep(0.01)
sys.exit(1)

for i in range(1, 127):
	for j in [0x80, 0, i, 0]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)

for i in range(1, 127):
	for j in [0x80, i, 0, 0]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)
 
for i in range(1, 127):
	for j in [0x80, i, i, 0]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)

for i in range(1, 127):
	for j in [0x80, 0, i, i]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)

for i in range(1, 127):
	for j in [0x80, i, 0, i]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)


for i in range(1, 127):
	for j in [0x80, i, i, i]:
		ser.write(chr(j))
	time.sleep(math.exp(-i/500)*0.07)

time.sleep(1)

ser.close()
