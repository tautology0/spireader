from memoryreader import app
from memoryreader.libraries import spiutils
from memoryreader.libraries import i2cutils
from flask import Response

# API routes
# SPI
@app.route('/api/spi/identify')
def spiidentify():
 spiutils.init("/dev/spidev0.0")
 return Response(spiutils.identify(), status=200, mimetype='application/json')

@app.route('/api/spi/read/<int:start>/<int:end>')
def spireadmem(start, end):
 spiutils.init("/dev/spidev0.0")
 return Response(spiutils.readmemory(start,end), status=200, mimetype='application/octet-stream')

# I2C
@app.route('/api/i2c/read/<int:start>/<int:end>')
def i2creadmem(start, end):
 i2cutils.init("1")
 return Response(i2cutils.readmemory(start,end), status=200, mimetype='application/octet-stream')
