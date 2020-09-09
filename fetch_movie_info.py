import json
import logging
from html.parser import HTMLParser
from time import sleep

from tqdm import tqdm

from strings import MOVIE_BASE_URL
from utils import threshold, fetch

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class MovieParser(HTMLParser):
    current_target = ''
    result = {}

    def handle_data(self, data):
        if data == '导演：':
            self.current_target = 'director'
        elif data == '编剧：':
            self.current_target = 'screenWriter'
        elif data == '国家地区：':
            self.current_target = 'location'
        elif data == '制作公司：':
            self.current_target = 'company'
        elif data == '更多片名：':
            self.current_target = 'alias'
        elif self.current_target != '':
            stripped = data.strip()
            if len(stripped) > 0 and stripped != '...':
                if self.current_target in self.result:
                    self.result[self.current_target].append(data)
                else:
                    self.result[self.current_target] = [data]

    def handle_endtag(self, tag):
        if tag == 'dd':
            self.current_target = ''

    def parse(self, data: str):
        self.current_target = ''
        self.result = {}
        self.feed(data)
        return self.result

    def error(self, message):
        logging.error(message)


parser = MovieParser()
result = []

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold + 1):
        try:
            info = parser.parse(fetch(str.format(MOVIE_BASE_URL, movie['id'])))
            info['id'] = movie['id']
            result.append(info)
            sleep(2)
            if i > 0 and i % 400 == 0:
                with open('raw/info/checkpoint_%d.json' % i, 'w', encoding='utf-8') as g:
                    json.dump(result, g, ensure_ascii=False)
            if i > threshold:
                break
        except Exception as e:
            logging.error(e)

with open('data/movie_info.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
