# news_maker
Parsing News articles for NLP

# todo
- Parse Rss feed and extract news article - DONE
- Scheduler for automated re-run of parsing script - DONE
- API endpoint for querying parsed news articles - NEEDS WORK
- Setup NPL module to process articles
  - Classify news into appropriate category
  - Classify into local vs global
  - Determine entities in each article ( Person, Org, Location )
  - Perform sentiment analysis

# setup
- Setup Mongo DB with username / password
- Clone Repo
- `cd` into the repo directory & run `pip3 install -r requirements.txt`
- Copy flask.cfg.sample as flask.cfg > update necessary config values
- Start using `python3 index.py`

# mongodb setup
- Docker: docker run -v /var/data/mongodb:/data/db -p 27017:27017 --name mymongo -d mongo mongod --smallfiles
  - replace `/var/data/mongodb` with volume share for docker on your local machine or server
```
db.createUser(
  {
    user: "<username_here>",
    pwd: "<password_here>",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ],
    passwordDigestor : "server"
  }
)

mongo admin -u "<username_here>" -p "<password_here>"
```
