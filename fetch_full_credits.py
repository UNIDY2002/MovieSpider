import json
import logging
import re
from html.parser import HTMLParser
from time import sleep

from tqdm import tqdm

from strings import FULL_CREDITS_URL
from utils import fetch, threshold

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class FullCreditParser(HTMLParser):
    actor_tit_activated = False
    force_stop = False
    actor_ids = []

    def handle_starttag(self, tag, attrs):
        if not self.force_stop:
            if ('class', 'credits_r') in attrs:
                self.force_stop = True
            elif ('class', 'actor_tit') in attrs:
                self.actor_tit_activated = True
            elif self.actor_tit_activated and tag == 'a':
                for x, y in attrs:
                    if x == 'href':
                        r = re.findall('http://people.mtime.com/(.+)/', y)
                        if len(r) > 0 and r[0] not in self.actor_ids:
                            self.actor_ids.append(r[0])

    def parse(self, data: str) -> [str]:
        self.actor_tit_activated = False
        self.force_stop = False
        self.actor_ids = []
        self.feed(data)
        return self.actor_ids

    def error(self, message):
        logging.error(message)


parser = FullCreditParser()

result = []

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold):
        actors = parser.parse(fetch(str.format(FULL_CREDITS_URL, movie['id'])))
        result.append((movie['id'], actors))
        sleep(8)
        if i > threshold:
            break

with open('data/full_credits.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
