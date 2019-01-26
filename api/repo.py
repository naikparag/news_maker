import jsonpickle
import json
import datetime
import pymongo
import api.db as db

def save(object):
    dbConn = db.getDb()
    try:
        collection = getCollectionName(object)
        data = json.loads(jsonpickle.encode(object, unpicklable=False))
        data["last_modified"] = datetime.datetime.utcnow()
        dbConn[collection].insert_one(data)
    except Exception as ex:
        print('repo - exception: ' + str(ex))

def findOne(object, key, value):
    dbConn = db.getDb()
    try:
        collection = getCollectionName(object)
        return dbConn[collection].find_one({key: value})
    except Exception as ex:
        print('repo - exception: ' + str(ex))
    return None

def find(collection, select='', limit=20, filter={}):
    dbConn = db.getDb()
    try:
        return dbConn[collection].find(filter, select).limit(limit).sort('last_modified', pymongo.DESCENDING)
    except Exception as ex:
        print('repo - exception: ' + str(ex))
    return None

def getStats():
    dbConn = db.getDb()
    try:
        return dbConn['Post'].aggregate([
            {'$group' : {'_id':'$source', 'count':{'$sum':1}}}
        ])
    except Exception as ex:
        print('repo - exception: ' + str(ex))
    return None

def getCollectionName(object):
    return str(type(object).__name__)