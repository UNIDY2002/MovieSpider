import json
import logging
from time import sleep

from tqdm import tqdm

from strings import *
from utils import fetch

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


movie_list = []
for i in tqdm(range(1, 523)):
    current_page = json.loads(fetch(str.format(MOVIE_LIST_URL, i)))['movieIntegrateList']
    for item in current_page:
        movie_list.append({
            'id': item['movieId'],
            'title': item['titleCn'],
            'year': item['year'],
            'actorId1': item['actorId1'],
            'actorName1': item['actorNameCn1'],
            'actorId2': item['actorId2'],
            'actorName2': item['actorNameCn2'],
            'genre': item['genreTypes'],
            'time': item['commonRuntime'],
            'rating': item['ratingFinal'] if 'ratingFinal' in item else None,
            'img': item['coverPath'],
        })
    sleep(1)

logging.info('Fetched %d movies.' % len(movie_list))

with open('data/movie_list.json', 'w', encoding='utf8') as f:
    json.dump(movie_list, f, ensure_ascii=True)
