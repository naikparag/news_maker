import csv
import feedparser
from newspaper import Article

import api.logger as apiLogger
logger = apiLogger.getLogger(__name__)
import api.repo as repo

def processRSSCsv(inputFile):
    logger.info('processinng input file: {file}'.format(file=inputFile))
    global output
    output = []
    with open(inputFile, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            processRSSUrl(row['url'], row['source'])
    return output

def processRSSUrl(url, source):
    newsFeed = feedparser.parse(url)
    logger.info('processing {count} entries for feed: {url}'.format(count=str(len(newsFeed.entries)), url=url))
    skipCount = 0
    for entry in newsFeed.entries:
        post = Post(entry.title, entry.link, entry.published, source)
        existingPost = repo.findOne(post, 'link', post.link)
        if existingPost is None:
            post = processNews(post)
            output.append(post)
            repo.save(post)
        else:
            skipCount += 1
    logger.info('skipping {count} entries for feed: {rssUrl}'.format(count=skipCount, rssUrl=url))

def processNews(post):
    article = Article(post.link)
    article.download()
    article.parse()
    post.setPostDetails(article.text, article.authors, article.top_image)
    return post

class Post(object):
    def __init__(self, title, link, published, source):
        self.title = title
        self.link = link
        self.published = published
        self.source = source

    def setPostDetails(self, text, authors, image):
        self.text = text
        self.authors = authors
        self.image = image