#!/usr/bin/env python

from periphery import SPI

class Jedec:
 def __init__(self, device):
  self.spi=SPI(device, 0, 24000000)
 
 def sendit(self, request,resplen):
  # Padding for response data
  buffer=request + [0] * resplen
  reqlen=len(request)

  # send the data and get the response
  response=self.spi.transfer(buffer)
  return response[reqlen:] 

 def RDID(self):
  response={}
  # op code 0x9f, response 3 bytes
  data=self.sendit([0x9f], 6)

  # First byte - manufacturer ID
  response['manufacturer']=[]
  i=1
  response['manufacturer'].append(data[0])
  if (chr(data[0]) == 0x7f):
   response['manufacturer'].append(data[i])
   i+=1
  if (chr(data[1]) == 0x7f):
   response['manufacturer'].append(data[i])
   i+=1
  if (chr(data[2]) == 0x7f):
   response['manufacturer'].append(data[i])
   i+=1
  response['type']=data[i]
  response['density']=data[i+1]
  return response

 def RES(self):
  response={}
  # op code 0xAB, response 3 bytes
  data=self.sendit([0xAB,0,0,0], 1)

  # First byte - manufacturer ID
  response['density']=chr(data[0])
  return response

 def REMS(self):
  response={}
  # op code 0x90, response 2 bytes
  data=self.sendit([0x90,0,0], 2)

  # First byte - manufacturer ID
  response['manufacturer']=chr(data[0])
  response['device']=chr(data[1])
  return response

 def RDSCUR(self):
  response={}
  data=self.sendit([0x2B], 1)

  response['security']=chr(data[0])
  return response

 def RDSR(self):
  response={}
  data=self.sendit([0x05], 1)

  response['status']=chr(data[0])
  return response

 def READ(self, address, length):
  # op code 0x03
  request=[0x03]

  # address is 3 bytes
  request.append((address & 0xff0000) >> 16) 
  request.append((address & 0xff00) >> 8) 
  request.append(address & 0xff) 
  data=self.sendit(request, length)

  return ''.join(chr(x) for x in data)
  
 def RAW(self, data, length):
  # op code 0x03
  request=data

  # address is 3 bytes
  d=self.sendit(request, length)
  print request

  return ''.join(chr(x) for x in d)

 def WREN(self):
  # op code 06
  d=self.sendit([0x06],0)

 def RST(self):
  # op code 00
  d=self.sendit([0x00],0)

 def WRDI(self):
  # op code 04
  d=self.sendit([0x04],0)

 def PP(self, address, data):
  # op code 02
  request=[0x2]
  
