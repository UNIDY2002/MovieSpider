import json

people_set = set()

with open('data/full_credits.json', encoding='utf-8') as f:
    for movie, people in json.load(f):
        for person in people[:10]:
            people_set.add(person)

with open('data/people_list.txt', 'w', encoding='utf-8') as f:
    for person in people_set:
        f.write('%s\n' % person)
