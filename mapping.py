import json

movie_map = {}

with open('data/movie_list.json', encoding='utf-8') as f:
    for movie in json.load(f):
        if movie['id'] not in movie_map:
            movie_map[movie['id']] = len(movie_map)

with open('data/movie_mapping.txt', 'w', encoding='utf-8') as f:
    for key in movie_map:
        f.write('%s %s\n' % (key, movie_map[key]))

actor_map = {}

with open('data/people_list.txt', encoding='utf-8') as f:
    for person in f:
        actor = person.strip()
        if actor not in actor_map:
            actor_map[actor] = len(actor_map)

with open('data/actor_mapping.txt', 'w', encoding='utf-8') as f:
    for key in actor_map:
        f.write('%s %s\n' % (key, actor_map[key]))
