# spireader
pre-pre-pre-alpha for a web based spireader designed for a Pi, but should work on a BBB or any Linux with spidev. The path is hardcoded to spidev0.0 at the moment and the speed to 24 MHz.

To start, run start.py which will run flask on 5000/tcp.

To automatically grab the whole chip (similar to flashrom) go to the root page and click "readit".

For the api:
/api/identify, returns a JSON containing the dump of the JEDEC identification of the chip, after a bit of mangulation (e.g. attempt to translate the manufacturer and to return the real capacity instead of the power). Continuation codes haven't been tested yet.
/api/read/start/end, reads from start to end. This should buffer it in blocks of 10KB, so shouldn't fall a foul of kernel limitations.

PRs and suggestions welcomed. Including those for a better name.

Plans are to add other modes, such as I2C, one wire, three wire, even a uboot md reader.
