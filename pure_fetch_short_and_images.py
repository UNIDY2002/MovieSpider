import json
from time import sleep

from tqdm import tqdm

from strings import SHORT_URL, IMAGES_URL
from utils import threshold, fetch

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for i, movie in tqdm(enumerate(movies), total=threshold):
        with open('raw/short/%d.html' % movie['id'], 'w', encoding='utf-8') as g:
            g.write(fetch(str.format(SHORT_URL, movie['id'])))
        sleep(5)
        with open('raw/images/%d.html' % movie['id'], 'w', encoding='utf-8') as g:
            g.write(fetch(str.format(IMAGES_URL, movie['id'])))
        sleep(5)
        if i > threshold:
            break
