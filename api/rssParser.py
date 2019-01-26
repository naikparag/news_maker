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
    return 'processing complete.'

def processRSSUrl(url, source):
    newsFeed = feedparser.parse(url)
    logger.info('processing {count} entries for feed: {url}'.format(count=str(len(newsFeed.entries)), url=url))
    skipCount = 0
    for entry in newsFeed.entries:
        published = ''
        if hasattr(entry, 'published'):
            published = entry.published
        post = Post(entry.title, entry.link, published, source)
        existingPost = repo.findOne(post, 'link', post.link)
        if existingPost is None:
            try:
                post = processNews(post)
                output.append(post)
                repo.save(post)
            except Exception as ex:
                print('ex handling for {url}: {error}'.format(url=post.link, error=str(ex)))
                skipCount += 1
        else:
            skipCount += 1
    logger.info('skipping {count} entries for feed: {rssUrl}'.format(count=skipCount, rssUrl=url))

def processNews(post):
    try:
        article = Article(post.link)
        article.download()
        article.parse()
        post.setPostDetails(article.text, article.authors, article.top_image)
        return post
    except Exception:
        raise
    return None

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