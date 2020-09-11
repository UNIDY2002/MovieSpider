import json

info_map = {}

with open('data/actor_info.json', encoding='utf-8') as f:
    info_list = json.load(f)
    for info in info_list:
        info_map[info['id']] = info

actor_map = {}

with open('data/people_list.txt', encoding='utf-8') as f:
    people = sorted([x.strip() for x in f],
                    key=lambda x: 0
                    if x in info_map and info_map[x]['photo'] != '' and info_map[x]['biography'] != ''
                    else 1)
    for person in people:
        if person not in actor_map:
            actor_map[person] = len(actor_map)
