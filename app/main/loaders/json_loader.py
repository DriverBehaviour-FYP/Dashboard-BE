import json


def load_json_path(path):
    with open(path, 'r') as f:
        return json.load(f)

