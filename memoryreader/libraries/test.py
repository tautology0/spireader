#!/usr/bin/python
from jedec import Jedec

spi=Jedec("/dev/spidev0.0")
fred=spi.RDID()
print fred
jim=spi.READ(0,100)
print jim
