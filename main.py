import csv
import feedparser
import jsonpickle
from newspaper import Article
from flask import Flask
app = Flask(__name__)

output = []

@app.route("/")
def index():
    return "Helllo news maker!"

@app.route("/rss")
def rss():
    parsedData = readURLCsv()
    result = {
        "result" : parsedData
    }
    return jsonpickle.encode(result, unpicklable=False)

def readURLCsv():
    with open('news_rss_url.txt', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        global output
        output = []
        for row in csv_reader:
            url = row['url']
            source = row['source']
            parseRssUrl(url, source)
    return output

def parseRssUrl(url, source):
    newsFeed = feedparser.parse(url)
    print ('Number of RSS posts :' + str(len(newsFeed.entries)))
    for entry in newsFeed.entries:
        post = Post(entry.title, entry.link, entry.published, source)
        post.article = parseNewsArticle(post.link)
        output.append(post)


def parseNewsArticle(url):
    article = Article(url)
    article.download()
    article.parse()
    return NewsArticle(article.text, article.authors, article.top_image)

class Post(object):
    def __init__(self, title, link, published, source):
        self.title = title
        self.link = link
        self.published = published
        self.source = source

class NewsArticle(object):
    def __init__(self, text, authors, image):
        self.text = text
        self.authors = authors
        self.image = image

if __name__ == '__main__':
    app.run(host='localhost', port=9300, debug=True)
