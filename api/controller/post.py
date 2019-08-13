import api.repo as repo
from flask import url_for

import api.logger as apiLogger
logger = apiLogger.getLogger(__name__)

def getPosts(limit, page):
    result = repo.find("Post", { 'title': 1, 'text': 1, 'link': 1 }, int(limit), int(page))
    return result

def getPostForDemo(limit, page):

    result = getPosts(limit, page)
    postDict = dict(result[0])
    postDict['title'] = postDict.get('title', '')
    postDict['text'] = postDict.get('text', '')
    # postDict['demoText'] = postDict.get('title', '') + '\n' + postDict.get('text', '')
    if page > 1:
        previousPost = url_for('demo', limit=limit, page=page-1, _external=True)
    else :
        previousPost = url_for('demo', limit=limit, page=page, _external=True)
    nextPost = url_for('demo', limit=limit, page=page+1, _external=True)

    return postDict, previousPost, nextPost