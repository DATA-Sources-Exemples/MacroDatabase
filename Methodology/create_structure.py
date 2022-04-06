import json

import os

try:
    path_str = "Database"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"


def path_to_dict(path, tree=None, json_containers=None, previous_path=None):
    if tree is None:
        tree = {}
    if json_containers is None:
        json_containers = {}

    name = os.path.basename(path)

    if ".json" not in name and "README.md" not in name:
        print(f"Creating structure for {path}")

    if os.path.isdir(path):
        if name not in tree and name != "Discontinued":
            tree[name] = {}

        for file in os.listdir(path):
            if file == "Discontinued":
                continue
            path_to_dict(path=os.path.join(path, file), tree=tree[name],
                         json_containers=json_containers, previous_path=path)
    else:
        if ".json" in name:
            if previous_path not in json_containers:
                json_containers[previous_path] = []
            json_containers[previous_path].append(name)

            tree[name] = None

    return tree, json_containers


tree, json_containers = path_to_dict(path_str)

if "Structure" not in os.listdir("../"):
    os.mkdir(f"Structure")

countries = list(tree['Database']['International Data']['Countries'].keys())
countries.remove("ID.json")
countries.sort()

states = list(tree['Database']['U.S. Regional Data']['States'].keys())
states.remove("ID.json")
states.sort()

json.dump(tree, open(f"../Structure/directory_structure.json", "w"), indent=2)
json.dump(json_containers, open(f"../Structure/json_structure.json", "w"), indent=2)
json.dump(countries, open(f"../Structure/countries.json", "w"), indent=2)
json.dump(states, open(f"../Structure/states.json", "w"), indent=2)
