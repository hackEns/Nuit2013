# TODO :
# stty -hup -F /dev/ttyUSB0

# ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1)

# ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 115200)

import serial
import time


def get_color(r, g, b) : # R/G/B : int [0, 255]
  # TODO : coeffs
  return [r / 2, g / 2, b / 2]


def send_color(ser, r, g, b) :
  for i in [0x80].append(get_color(r, g, b)) :
    ser.write(chr(i))
    # TODO : time.sleep(0.01) ?


def main() :
  ser = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 115200,
    # parity = serial.PARITY_NONE,
    # stopbits = serial.STOPBITS_ONE,
    # bytesize = serial.EIGHTBITS,
    # timeout = 1
    )

  #ser.close()
  # ser.open()

  # if (not ser.isOpen()):
  #   print "NOT open"
  #   exit

  # for i in range(1, 100):
  #   ser.write(chr(i)) # Cela devrait bien envoyer seulement un octet (*devrait*...)
  #   #print "Sent " + str(i) + ", read " + (ord(ser.read(1)))
  #   print ser.read(1000)
    
    
  for i in range(0, 127) :
    send_color(ser, i, i, i)
    # for j in [0x80, i, i, 0]:
    #   ser.write(chr(j))

  # print ser.readlines()

  ser.close()


main()