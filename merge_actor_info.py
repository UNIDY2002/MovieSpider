import json
import logging

from tqdm import tqdm

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

actor_map = {}

with open('data/people_list.txt', encoding='utf-8') as f:
    for person in f:
        actor = person.strip()
        if actor not in actor_map:
            actor_map[actor] = len(actor_map)

collaboration_graph = [[0] * len(actor_map) for _ in range(len(actor_map))]

logging.info('There are altogether %d actors counted.' % len(actor_map))

with open('data/full_credits.json', encoding='utf-8') as f:
    for movie, actors in json.load(f):
        actors = [actor_map[actor] for actor in actors[:10]]
        for i in range(len(actors) - 1):
            for j in range(i + 1, len(actors)):
                collaboration_graph[actors[i]][actors[j]] += 1
                collaboration_graph[actors[j]][actors[i]] += 1

dense_graph = [[x for x, y in sorted(enumerate(actor_row), key=lambda x: -x[1])[:10] if y > 0]
               for actor_row in tqdm(collaboration_graph)]

with open('data/actor_info.json', encoding='utf-8') as f:
    actors = json.load(f)
    for i, actor in enumerate(actors):
        actor['id'] = actor_map[actor['id']]
        actor['collaborators'] = dense_graph[actor['id']]

with open('data/actor_merged.json', 'w', encoding='utf-8') as g:
    json.dump(actors, g)

logging.info('Finally, information about %d actors are saved.' % len(actors))
