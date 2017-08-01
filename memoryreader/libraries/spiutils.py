#!/usr/bin/env python

import json
from jedec import Jedec

manufacturer_first = {
 0x01:"AMD", 0x02:"AMI", 0x83:"Fairchild", 0x04:"Fujitsu",
 0x85:"GTE", 0x86:"Harris", 0x07:"Hitachi", 0x08:"Inmos",
 0x89:"Intel", 0x8A:"I.T.T.", 0x0B:"Intersil", 0x8C:"Monolithic Memories",
 0x0D:"Mostek", 0x0E:"Motorola", 0x8F:"National", 0x10:"NEC",
 0x91:"RCA", 0x92:"Raytheon", 0x13:"Conexant (Rockwell)", 0x94:"Seeq",
 0x15:"Philips Semi. (Signetics)", 0x16:"Synertek", 0x97:"Texas Instruments",
 0x98:"Toshiba", 0x19:"Xicor", 0x1A:"Zilog", 0x9B:"Eurotechnique",
 0x1C:"Mitsubishi", 0x9D:"Lucent (AT&T)", 0x9E:"Exel", 0x1F:"Atmel",
 0x20:"SGS/Thomson", 0xA1:"Lattice Semi.", 0xA2:"NCR",
 0x23:"Wafer Scale Integration", 0xA4:"IBM", 0x25:"Tristar", 0x26:"Visic",
 0xA7:"Intl. CMOS Technology", 0xA8:"SSSI", 0x29:"Microchip Technology",
 0x2A:"Ricoh Ltd.", 0xAB:"VLSI", 0x2C:"Micron Technology",
 0xAD:"Hyundai Electronics", 0xAE:"OKI Semiconductor", 0x2F:"ACTEL",
 0xB0:"Sharp", 0x31:"Catalyst", 0x32:"Panasonic", 0xB3:"IDT", 0x34:"Cypress",
 0xB5:"DEC", 0xB6:"LSI Logic", 0x37:"Zarlink (formerly Plessey)", 0x38:"UTMC",
 0xB9:"Thinking Machine", 0xBA:"Thomson CSF", 0x3B:"Integrated CMOS (Vertex)",
 0xBC:"Honeywell", 0x3D:"Tektronix", 0x3E:"Sun Microsystems", 0xBF:"SST",
 0x40:"MOSEL", 0xC1:"Infineon (formerly Siemens)", 0xC2:"Macronix",
 0x43:"Xerox", 0xC4:"Plus Logic", 0x45:"SunDisk", 0x46:"Elan Circuit Tech.",
 0xC7:"European Silicon Str.", 0xC8:"Apple Computer", 0xC9:"Xilinx",
 0x4A:"Compaq", 0xCB:"Protocol Engines", 0x4C:"SCI", 0xCD:"Seiko Instruments",
 0xCE:"Samsung", 0x4F:"I3 Design System", 0xD0:"Klic", 0x51:"Crosspoint Solutions",
 0x52:"Alliance Semiconductor", 0xD3:"Tandem", 0x54:"Hewlett-Packard",
 0xD5:"Intg. Silicon Solutions", 0xD6:"Brooktree", 0x57:"New Media",
 0x58:"MHS Electronic", 0xD9:"Performance Semi.", 0xDA:"Winbond Electronic",
 0x5B:"Kawasaki Steel", 0xDC:"Bright Micro", 0x5D:"TECMAR", 0x5E:"Exar",
 0xDF:"PCMCIA", 0xE0:"LG Semiconductor", 0x61:"Northern Telecom", 0x62:"Sanyo",
 0xE3:"Array Microsystems", 0x64:"Crystal Semiconductor", 0xE5:"Analog Devices",
 0xE6:"PMC-Sierra", 0x67:"Asparix", 0x68:"Convex Computer",
 0xE9:"Quality Semiconductor", 0xEA:"Nimbus Technology", 0x6B:"Transwitch",
 0xEC:"Micronas (ITT Intermetall)", 0x6D:"Cannon", 0x6E:"Altera", 0xEF:"NEXCOM",
 0x70:"QUALCOMM", 0xF1:"Sony", 0xF2:"Cray Research", 0x73:"AMS(Austria Micro)",
 0xF4:"Vitesse", 0x75:"Aster Electronics", 0x76:"Bay Networks(Synoptic)",
 0xF7:"Zentrum or ZMD", 0xF8:"TRW", 0x79:"Thesys", 0x7A:"Solbourne Computer",
 0xFB:"Allied-Signal", 0x7C:"Dialog", 0xFD:"Media Vision",
 0xFE:"Level One Communication" }

def init(device):
 global spi
 spi=Jedec(device)
 
def identify():
 # reset chip first
 spi.RST()
 rdid=spi.RDID()
 output={}

 # manufacturer lookup
 i=0
 while rdid['manufacturer'][i] == chr(0x7f):
  i+=1

 if rdid['manufacturer'][i] == '\x00' or rdid['manufacturer'][i] == '\xff':
  raise('Illegal Response Returned')

 output['manufacturer']=manufacturer_first[rdid['manufacturer'][i]]

 # ID15-ID8 should be 0x40 for SPI NOR Flash
# if rdid['type'] != 0x40 or rdid['type'] != 0x20:
#  raise('Unknown memory type')
 output['type']=rdid['type']

 # ID7-ID0 should be the size of the chip (we hope, we love standards we do)
 output['capacity']=2 ** rdid['density']

 return json.dumps(output)
 
def readmemory(start, end):
 # reads a chunk of memory - buffers into pages to account for the GPI driver
 # As we're trying to be stateless we'll trust the client

 # guess a suitable blocksize
 blocksize=10240

 # reset chip first
 spi.RST()

 # Just allocate the whole size in advance - should not cause a problem with most chips
 buffer=b''
 transfer=b''

 while start < end:
  toread=1024
  if end-start < 1024:
   toread=end-start
  transfer=spi.READ(start, toread)
  buffer += transfer
  start+=toread

 return buffer 
 

def RES(self):
 response={}
 # op code 0xAB, response 3 bytes
 data=self.sendit([0xAB,0,0,0], 1)

 # First byte - manufacturer ID
 response['device']=chr(data[0])
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

def READ(self, faddress, length):
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

def WRDI(self):
 # op code 04
 d=self.sendit([0x04],0)

def PP(self, address, data):
 # op code 02
 request=[0x2]
  
if __name__ == "__main__":
 import hexdump
 init("/dev/spidev0.0")
 fred=identify()
 print fred
 jim=readmemory(0,1048576)
 hexdump.hexdump(jim)
