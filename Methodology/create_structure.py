import json

import os

try:
    path_str = "Database"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"


def path_to_dict(path, tree=None, json_containers=None, json_containers_discontinued=None, previous_path=None):
    if tree is None:
        tree = {}
    if json_containers is None:
        json_containers = {}
    if json_containers_discontinued is None:
        json_containers_discontinued = {}

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
                         json_containers=json_containers, json_containers_discontinued=json_containers_discontinued,
                         previous_path=path)
    else:
        if "_" in name and ".json" in name:
            paths = previous_path.split("/")
            exclusions_name = os.listdir(path_str)
            exclusions_path = ['..', 'Database']
            exclusions_name.extend(exclusions_path)

            name_path = previous_path.split("/")
            for directory in exclusions_name:
                if directory in name_path:
                    name_path.remove(directory)
            for directory in exclusions_path:
                if directory in paths:
                    paths.remove(directory)

            if "Discontinued" in name:
                variable_name = f"{'/'.join(name_path)} [Discontinued]"
            else:
                variable_name = f"{'/'.join(name_path)}"

            location = f"{previous_path}/{name}"

            if json.load(open(location, "r")):
                if "Discontinued" in variable_name:
                    json_containers_discontinued[variable_name] = f"{'/'.join(paths)}/{name}"
                else:
                    json_containers[variable_name] = f"{'/'.join(paths)}/{name}"

            tree[name] = None

    return tree, json_containers, json_containers_discontinued


tree, json_containers, json_containers_discontinued = path_to_dict(path_str)

if "Structure" not in os.listdir("../"):
    os.mkdir(f"Structure")

countries = list(tree['Database']['International Data']['Countries'].keys())

if "ID.json" in countries:
    countries.remove("ID.json")
if "_Countries.json" in countries:
    countries.remove("_Countries.json")

countries.sort()

states = list(tree['Database']['U.S. Regional Data']['States'].keys())

if "ID.json" in states:
    states.remove("ID.json")
if "_States.json" in states:
    states.remove("_States.json")

states.sort()

json.dump(tree, open(f"../Structure/directory_structure.json", "w"), indent=2)
json.dump(json_containers, open(f"../Structure/database_structure.json", "w"), indent=2)
json.dump(json_containers_discontinued, open(f"../Structure/database_discontinued_structure.json", "w"), indent=2)
json.dump(countries, open(f"../Structure/countries.json", "w"), indent=2)
json.dump(states, open(f"../Structure/states.json", "w"), indent=2)
