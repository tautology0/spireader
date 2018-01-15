#!/usr/bin/env python

import json
import RPi.GPIO as GPIO

# default pins
address = [ 27, 18, 17, 15, 14, 4, 3, 2, 22, 23, 24, 10, 9]
data = [ 21, 26, 20, 19, 16, 13, 6, 12 ]
ce = 25
oe = 11
pgm = 8

def init():
 GPIO.setmode(GPIO.BCM)
 GPIO.setwarnings(False)
 for i in address:
  GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
 for i in data:
  GPIO.setup(i, GPIO.IN)
 GPIO.setup(ce, GPIO.OUT, initial=GPIO.LOW)
 GPIO.setup(oe, GPIO.OUT, initial=GPIO.LOW)

def identify():
 # Not certain what to do here
 output={}

 return json.dumps(output)
def setaddr(a):
 for i, v in enumerate(address):
  if (a & (1<<i)):
   GPIO.output(v, GPIO.HIGH)
  else:
   GPIO.output(v, GPIO.LOW)

def readbyte(a):
 setaddr(a)
 # Now read from data
 result=0
 for i, v in enumerate(data):
  if GPIO.input(v) == GPIO.HIGH:
   result = result | (1<<i)
 return result

def readmemory(start, end):
 buffer=b''
 while start < end:
  buffer=buffer + chr(readbyte(start))
  start=start+1
 return buffer

if __name__ == "__main__":
 import hexdump
 init()
 jim=readmemory(0,8*1024)
 hexdump.hexdump(jim)
