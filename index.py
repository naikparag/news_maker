import jsonpickle
import logging

import api.rssParser as rssParser
import api.logger as apiLogger
logger = apiLogger.getLogger(__name__)

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('flask.cfg')

# ---- Decorator ----
from functools import wraps
from flask import request, abort
def validate_apikey(func):
    @wraps(func)
    def decoratedFunc(*args, **kwargs):
        print(request.headers.get('api-key'))
        print(request.args.get('api-key'))
        if (app.config['ADMIN_KEY'] == request.headers.get('api-key') 
        or app.config['ADMIN_KEY'] == request.args.get('api-key')):
            return(func(*args, **kwargs))
        else:
            abort(401)
    return decoratedFunc

# ---- Routes ----
@app.route("/")
@validate_apikey
def index():
    return "Helllo NEWS-MAKER!"

@app.route("/rss")
@validate_apikey
def rss():
    parsedData = rssParser.processRSSCsv()
    result = {
        "result" : parsedData
    }
    return jsonpickle.encode(result, unpicklable=False)

if __name__ == '__main__':
    app.run(host='localhost', port=app.config['PORT'], debug=app.config['DEBUG'])
