from app import app
from app.libraries import spiutils

spiutils.init("/dev/spidev0.0")

# API routes
@app.route('/api/identify')
def identify():
 return spiutils.identify()

@app.route('/api/read/<int:start>/<int:end>')
def readmem(start, end):
 return spiutils.readmemory(start,end)

# Web app routes

