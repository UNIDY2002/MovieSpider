import json
import logging

from tqdm import tqdm

from actor_mapping import actor_map

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

collaboration_graph = [[0] * len(actor_map) for _ in range(len(actor_map))]

with open('data/full_credits.json', encoding='utf-8') as f:
    for movie, actors in json.load(f):
        actors = [actor_map[actor] for actor in actors[:10]]
        for i in range(len(actors) - 1):
            for j in range(i + 1, len(actors)):
                collaboration_graph[actors[i]][actors[j]] += 1
                collaboration_graph[actors[j]][actors[i]] += 1

collaboration_graph = [[(x, y) for x, y in sorted(enumerate(actor_row), key=lambda x: -x[1])[:10] if y > 0]
                       for actor_row in tqdm(collaboration_graph)]

with open('data/collaboration_graph.json', 'w', encoding='utf-8') as f:
    json.dump(collaboration_graph, f)
