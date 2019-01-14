import jsonpickle
import logging

import api.rssParser as rssParser
import api.logger as apiLogger
logger = apiLogger.getLogger(__name__)

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('flask.cfg')

@app.route("/")
def index():
    return "Helllo NEWS-MAKER!"

@app.route("/rss")
def rss():
    parsedData = rssParser.processRSSCsv()
    result = {
        "result" : parsedData
    }
    return jsonpickle.encode(result, unpicklable=False)

if __name__ == '__main__':
    app.run(host='localhost', port=app.config['PORT'], debug=app.config['DEBUG'])
