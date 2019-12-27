from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

import api.rssParser as rssParser
import api.controller.post as postController
import api.db as db
import api.logger as apiLogger
logger = apiLogger.getLogger(__name__)

from flask import Flask, url_for

VERSION = 'v1.0.6'

# Scheduler
# --------------------
def rssScheduler(file):
    rssParser.processRSSCsv(file)

def initScheduler(file):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(rssScheduler, 'interval', minutes=30, id='scheduler_bg_rss_parser', args=[file])
    scheduler.start()
    return scheduler

# app
# --------------------

def create_app():
    app = Flask(__name__, template_folder='web', static_folder='web/static')
    app.config.from_pyfile('flask.cfg')
    db.initDb(app)
    scheduler = initScheduler(app.config['INPUT_RSS_FILE_PATH'])
    atexit.register(lambda: scheduler.shutdown(wait=False))
    return app

app = create_app()

import api.repo as repo

# Decorators
# --------------------
from functools import wraps
from flask import request, abort
def validate_apikey(func):
    @wraps(func)
    def decoratedFunc(*args, **kwargs):
        if (app.config['ADMIN_KEY'] == request.headers.get('api-key') 
        or app.config['ADMIN_KEY'] == request.args.get('api-key')):
            return(func(*args, **kwargs))
        else:
            abort(401)
    return decoratedFunc

# Routes
# --------------------
@app.route("/")
@validate_apikey
def index():
    return "NEWS-MAKER " + VERSION

@app.route("/post")
@validate_apikey
def getPost():
    limit = request.args.get('limit') or 20
    page = request.args.get('page') or 0
    result = postController.getPosts(limit, page)
    return dumps(result, json_options=RELAXED_JSON_OPTIONS)

@app.route("/rss")
@validate_apikey
def rss():
    inputfile = app.config['INPUT_RSS_FILE_PATH']
    parsedData = rssParser.processRSSCsv(inputfile)
    result = {
        "result" : parsedData
    }
    return dumps(result)

@app.route('/stats')
@validate_apikey
def getStats():
    result = repo.getStats()
    return dumps(result)

from flask import render_template
import api.controller.nlp as nlp
@app.route('/demo')
def demo():
    limit = int(request.args.get('limit') or 1)
    page = int(request.args.get('page') or 1)

    post, previousPost, nextPost = postController.getPostForDemo(limit, page)
    titleEntityHTML, textEntityHTML = nlp.nlp(post['title'], post['text'])

    bundle = { 
        'title': 'News-Maker Demo',
        'version': VERSION,
        'postTitle': post['title'],
        'postBody': post['text'],
        'postTitleNLP': titleEntityHTML,
        'postBodyNLP': textEntityHTML,
        'previousPost': previousPost,
        'nextPost': nextPost
    }
    return render_template('index.html', bundle=bundle)

# Main
# --------------------

if __name__ == '__main__':
    app.run(host='localhost', port=app.config['PORT'], debug=app.config['DEBUG'])
