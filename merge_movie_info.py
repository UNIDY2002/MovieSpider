import json
import logging

from actor_mapping import actor_map
from movie_mapping import movie_map

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

movie_dict = {}

with open('data/movie_list.json', encoding='utf-8') as f:
    movies = json.load(f)
    for movie in movies:
        movie['id'] = movie_map[movie['id']]
        movie['actorId1'] = actor_map[str(movie['actorId1'])] if str(movie['actorId1']) in actor_map else -1
        movie['actorId2'] = actor_map[str(movie['actorId2'])] if str(movie['actorId2']) in actor_map else -1
        movie.pop('actorName1')
        movie.pop('actorName2')
        if 'img' in movie and movie['img'] is not None:
            movie['img'] = movie['img'] if movie['img'].startswith('http') else 'https:' + movie['img']
        if movie['img'] is None:
            movie['img'] = ''
        if movie['rating'] is None:
            movie['rating'] = ''
        movie['genre'] = '|'.join(x.split('|')[1] for x in movie['genre'].split(';')) if movie['genre'] != '' else ''
        movie_dict[movie['id']] = movie

with open('data/movie_info.json', encoding='utf-8') as f:
    info_list = json.load(f)
    for info in info_list:
        if movie_map[info['id']] in movie_dict:
            movie = movie_dict[movie_map[info['id']]]
            for key in info:
                if key != 'id':
                    movie[key] = '|'.join(info[key])

with open('data/full_credits.json', encoding='utf-8') as f:
    for movie, actors in json.load(f):
        if movie_map[movie] in movie_dict:
            movie = movie_dict[movie_map[movie]]
            movie['actors'] = [actor_map[x] for x in actors[:10]]

for original_id in movie_map:
    if movie_map[original_id] in movie_dict:
        try:
            with open('data/plots/%s.json' % original_id, encoding='utf-8') as f:
                movie_dict[movie_map[original_id]]['plots'] = json.load(f)
        except FileNotFoundError:
            pass

        try:
            with open('data/reviews/%s.txt' % original_id, encoding='utf-8') as f:
                data = f.read()
                reviews = ['\n'.join(x.strip() for x in y.strip().split('headerheaderheader'))
                           for y in data.split('sepsepsep') if y.strip() != '']
                movie_dict[movie_map[original_id]]['reviews'] = reviews
        except FileNotFoundError:
            pass

with open('data/short.json', encoding='utf-8') as f:
    for movie, reviews in json.load(f):
        if movie_map[movie] in movie_dict:
            movie = movie_dict[movie_map[movie]]
            reviews.extend(movie['reviews'] if 'reviews' in movie else [])
            movie['reviews'] = reviews

result = [p for p in (movie_dict[x] for x in movie_dict) if 'actors' in p]

logging.info('A sum of %s movies are loaded.' % len(result))

with open('data/movie_merged.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)
