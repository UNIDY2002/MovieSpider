import json
import logging
import re
from html.parser import HTMLParser
from time import sleep

from tqdm import tqdm

from strings import PEOPLE_URL, BIOGRAPHY_URL
from utils import fetch

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class PersonParser(HTMLParser):
    name = ''
    activated = False
    photo_url = ''
    base_activated = False
    constellation = ''
    height = ''
    weight = ''
    born_activated = False
    birthday = ''
    birth_place = ''

    def handle_starttag(self, tag, attrs):
        if ('class', 'per_cover __r_c_') in attrs:
            self.activated = True
        elif ('class', 'per_base_star clearfix __r_c_') in attrs:
            self.base_activated = True
        elif ('class', 'per_base_born __r_c_') in attrs:
            self.born_activated = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            if self.activated:
                self.activated = False
                for x, y in attrs:
                    if x == 'src':
                        self.photo_url = y

    def handle_endtag(self, tag):
        if tag == 'dl':
            self.base_activated = False
            self.born_activated = False

    def handle_data(self, data):
        if self.base_activated:
            if data in ['白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '魔羯', '水瓶', '双鱼']:
                self.constellation = data
            elif re.match('\\d+cm', data):
                self.height = data
            elif re.match('\\d+kg', data):
                self.weight = data
        if self.born_activated:
            stripped = data.strip()
            if len(stripped) > 0:
                if re.match('\\d+-\\d+-\\d+', stripped):
                    self.birthday = stripped
                else:
                    self.birth_place = stripped
        if self.lasttag == 'h2' and self.name == '':
            self.name = data

    def parse(self, data: str) -> (str, str):
        self.name = ''
        self.activated = False
        self.photo_url = ''
        self.base_activated = False
        self.constellation = ''
        self.height = ''
        self.weight = ''
        self.born_activated = False
        self.birthday = ''
        self.birth_place = ''
        self.feed(data)
        return self.name, self.photo_url, self.constellation, self.height, self.weight, self.birthday, self.birth_place

    def error(self, message):
        logging.error(message)


class BiographyParser(HTMLParser):
    activated = False
    content = ''

    def handle_starttag(self, tag, attrs):
        if ('id', 'lblAllGraphy') in attrs:
            self.activated = True

    def handle_startendtag(self, tag, attrs):
        if self.activated and tag == 'br':
            self.content += '\n'

    def handle_data(self, data):
        if self.activated:
            self.content += data

    def handle_endtag(self, tag):
        if self.activated:
            if tag == 'p':
                self.content += '\n'
            elif tag == 'div':
                self.activated = False

    def parse(self, data: str) -> str:
        self.activated = False
        self.content = ''
        self.feed(data)
        return self.content.strip()

    def error(self, message):
        logging.error(message)


person_parser = PersonParser()
biography_parser = BiographyParser()

has_biography = 0

result = []

with open('data/people_list.txt', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in tqdm(enumerate(lines), total=len(lines)):
        person = line.strip()
        name, photo, constellation, height, weight, birthday, birth_place = \
            person_parser.parse(fetch(str.format(PEOPLE_URL, person)))
        sleep(1)
        biography = biography_parser.parse(fetch(str.format(BIOGRAPHY_URL, person)))
        if len(biography) > 0:
            has_biography += 1
        sleep(1)
        result.append({
            'name': name,
            'photo': photo,
            'constellation': constellation,
            'height': height,
            'weight': weight,
            'birthday': birthday,
            'birth_place': birth_place,
            'biography': biography,
        })
        if i > 0 and i % 400 == 0:
            with open('raw/actors/checkpoint_%d.json' % i, 'w', encoding='utf-8') as g:
                json.dump(result, g, ensure_ascii=False)
            logging.info('Up till now, %d out of %d actors have biography.' % (has_biography, i))

logging.info('A sum of %d actors have biography.' % has_biography)
with open('data/actor_info.json', 'w', encoding='utf-8') as g:
    json.dump(result, g)
