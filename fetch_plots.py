import json
import logging
from html.parser import HTMLParser
from time import sleep

from tqdm import tqdm

from strings import PLOTS_URL
from utils import fetch, threshold

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class PlotParser(HTMLParser):
    plots_box_depth = 0
    plots = []
    current = ''

    def handle_starttag(self, tag, attrs):
        if ('class', 'plots_box') in attrs or self.plots_box_depth > 0:
            self.plots_box_depth += 1

    def handle_data(self, data):
        if self.plots_box_depth > 0:
            self.current += data

    def handle_endtag(self, tag):
        if self.plots_box_depth > 0:
            self.plots_box_depth -= 1
            if self.plots_box_depth == 0:
                self.plots.append(self.current.strip())
                self.current = ''

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.current += '\n'

    def parse(self, data: str) -> [str]:
        self.plots = []
        self.feed(data)
        return self.plots

    def error(self, message):
        logging.error(message)


parser = PlotParser()

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold):
        plots = parser.parse(fetch(str.format(PLOTS_URL, movie['id'])))
        with open('data/plots/%s.json' % movie['id'], 'w', encoding='utf-8') as g:
            json.dump(plots, g)
        sleep(4)
        if i > threshold:
            break
