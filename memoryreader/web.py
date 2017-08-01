from memoryreader import app
from memoryreader.libraries import spiutils
import flask

# Web routes
@app.route('/')
@app.route('/index.html')
def index():
 return flask.render_template('index.html')

