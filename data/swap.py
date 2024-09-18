import json

with open('champions_name.json', 'r') as cn:
    champ_data = json.load(cn)

champs_by_key = dict()

for key, value in champ_data['data'].items():
    champs_by_key[value['key']] = value

# with open('champions.json', 'w') as json_file:
    # json.dump(champs_by_key, json_file)
print(champs_by_key)
