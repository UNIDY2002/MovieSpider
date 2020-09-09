import json
import logging
from html.parser import HTMLParser

from tqdm import tqdm

from utils import threshold

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class ShortParser(HTMLParser):
    comments = []

    def handle_data(self, data):
        if self.lasttag == 'h3' and len(data.strip()) > 0:
            self.comments.append(data)

    def parse(self, data: str) -> [str]:
        self.comments = []
        self.feed(data)
        return self.comments[:5]

    def error(self, message):
        logging.error(message)


parser = ShortParser()
result = []

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold):
        try:
            with open('raw/short/%d.html' % movie['id'], encoding='utf-8') as g:
                result.append((movie['id'], parser.parse('\n'.join(g.readlines()))))
        except Exception as e:
            logging.error(e)
        if i > threshold:
            break

with open('data/short.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
