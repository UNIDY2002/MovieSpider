import json

movie_map = {}

with open('data/movie_list.json', encoding='utf-8') as f:
    for movie in json.load(f):
        if movie['id'] not in movie_map:
            movie_map[movie['id']] = len(movie_map)
