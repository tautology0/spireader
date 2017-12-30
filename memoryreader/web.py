from memoryreader import app
import flask

# Web routes
@app.route('/spi.html')
def spi():
 return flask.render_template('spi.html')

@app.route('/i2c.html')
def i2c():
 return flask.render_template('i2c.html')

