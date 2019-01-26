from pymongo import MongoClient
db = None

def initDb(app):
    global db
    if db is None:
        try:
            mongoUrl = app.config['MONGO_URL']
            client = MongoClient(mongoUrl)
            db = client['news_maker']
            print('Initializing Database.....')

            db.Post.create_index('link', unique=True)
        except Exception as ex:
            print('db - exception: ' + str(ex))
    return db

def getDb():
    # add exception if null
    global db
    return db
