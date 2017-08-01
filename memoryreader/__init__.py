from flask import Flask

app=Flask(__name__)
# For testing
app.config['TEMPLATES_AUTO_RELOAD'] = True
from memoryreader import api
from memoryreader import web
