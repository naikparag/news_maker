import jsonpickle
import json

import api.db as db
dbConn = db.getDb()

def save(object):
    try:
        collection = getCollectionName(object)
        data = json.loads(jsonpickle.encode(object, unpicklable=False))
        dbConn[collection].insert_one(data)
    except Exception as ex:
        print(ex)

def findOne(object, key, value):
    try:
        collection = getCollectionName(object)
        return dbConn[collection].find_one({key: value})
    except Exception as ex:
        print(ex)
    return None

def getCollectionName(object):
    return str(type(object).__name__)

