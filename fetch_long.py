import json
import logging
from html.parser import HTMLParser
from time import sleep

from tqdm import tqdm

from strings import COMMENT_URL
from utils import threshold, fetch

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class CommentParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        if ('class', 'px12 ml6') in attrs:
            for x, y in attrs:
                if x == 'href' and y not in self.links:
                    self.links.append(y)

    def parse(self, data: str) -> [str]:
        self.links = []
        self.feed(data)
        return self.links[:2]

    def error(self, message):
        logging.error(message)


class ReviewParser(HTMLParser):
    content = ''
    content_activated = False
    header_activated = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.header_activated = True
        elif ('class', 'db_mediacont db_commentcont') in attrs:
            self.content_activated = True
        elif tag == 'div':
            self.content_activated = False
        elif tag == 'p':
            self.content += '\n'

    def handle_data(self, data):
        if self.content_activated or self.header_activated:
            self.content += data.strip()

    def handle_startendtag(self, tag, attrs):
        if self.content_activated and tag == 'br':
            self.content += '\n'

    def handle_endtag(self, tag):
        if tag == 'div':
            self.content_activated = False
        elif tag == 'h2':
            self.header_activated = False
            self.content += 'headerheaderheader'

    def parse(self, data: str, index: int) -> [str]:
        self.content = ''
        self.content_activated = False
        self.header_activated = False
        self.feed(data)
        sleep(3)
        if self.content.count('headerheaderheader') > 1:
            logging.error('Something wrong with %d.' % index)
        return self.content.strip()

    def error(self, message):
        logging.error(message)


comment_parser = CommentParser()

review_parser = ReviewParser()

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold):
        links = comment_parser.parse(fetch(str.format(COMMENT_URL, movie['id'])))
        doc = 'sepsepsep'.join(review_parser.parse(fetch(link), movie['id']) for link in links)
        if len(doc) > 0:
            with open('data/reviews/%d.txt' % movie['id'], 'w', encoding='utf-8') as g:
                g.write(doc)
        sleep(2)
        if i > threshold:
            break
