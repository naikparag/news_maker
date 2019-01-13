from pymongo import MongoClient
db = None

def getDb():
    global db
    if db is None:
        try:
            client = MongoClient('localhost:27017')
            db = client['news_maker']
            print('Initializing Database.....')

            db.Post.create_index('link', unique=True)
        except Exception as ex:
            print(ex)
    return db