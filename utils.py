import json


def get_id_employers():
    with open('employers.json', 'r') as f:
        get_employers = json.load(f)
        for employee in range(len(get_employers)):
            id = get_employers[employee]['id']
            print(id)
