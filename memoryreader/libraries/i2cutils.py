#!/usr/bin/env python

import json
import smbus2
import RPi.GPIO

def init(device):
 global i2c
 i2c=smbus2.SMBus(device)
 
def identify():
 # We should probe for address here really.
 output={}

 return json.dumps(output)

def readblock(address):
 # Reads an SMBus block (32 bytes) and returns it as a binary string
 # I2C address is hard coded for the moment
 # Assuming it's 16 bit address mode
 w=smbus2.i2c_msg.write(0x50,[address/256, address%256])
 r=smbus2.i2c_msg.read(0x50, 32)
 i2c.i2c_rdwr(w,r)
 return ''.join(chr(x) for x in list(r))
 
def readmemory(start, end):
 # reads a chunk of memory - we have to do this in blocks of 32 bytes
 # thanks to SMBus

 # assume we're using address 0x50 - i.e. all address pins are forced to ground
 # We should probably take this as a user parameter

 # Just allocate the whole size in advance - should not cause a problem with most chips
 buffer=b''
 transfer=b''

 while start < end:
  transfer=readblock(start)
  buffer += transfer
  start+=32

 return buffer 

if __name__ == "__main__":
 import hexdump
 init(1)
 jim=readmemory(0,16*1024)
 hexdump.hexdump(jim)
