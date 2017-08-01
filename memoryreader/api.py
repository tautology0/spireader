from memoryreader import app
from memoryreader.libraries import spiutils
from flask import Response

# API routes
@app.route('/api/identify')
def identify():
 spiutils.init("/dev/spidev0.0")
 return Response(spiutils.identify(), status=200, mimetype='application/json')

@app.route('/api/read/<int:start>/<int:end>')
def readmem(start, end):
 spiutils.init("/dev/spidev0.0")
 return Response(spiutils.readmemory(start,end), status=200, mimetype='application/octet-stream')

