import json
import os

import fred

from config import misc


def obtain_series_data(name, data):
    try:
        print(f"Attempting {name} ({data['id']})")
        fred_id = data['id']
        children = fred.category_series(fred_id)['seriess']

        if "Discontinued" not in os.listdir(data['path']):
            os.mkdir(f"{data['path']}/Discontinued")

        for series in children:
            if "DISCONTINUED" in series['title']:
                path = f"{data['path']}/Discontinued/{series['id']}.json"
            else:
                path = f"{data['path']}/{series['id']}.json"

            json.dump(series, open(path, "w"))
            print(f"Collected {series} for {data['name']}")
    except KeyError:
        return print(f"Not able to collect data for {name}")


json_data = {}
fred.key(misc[214][43:75])
for file in os.listdir("IDs"):
    if file == "_IDs.json":
        continue
    json_data[file.strip(".json")] = json.load(open(f"IDs/{file}", "r"))
json.dump(sorted(json_data), open(f"IDs/_IDs.json", "w"), indent=2)

path = "Data"
children_directories = {}

for directory_path, directory_names, _ in os.walk(path):
    if len(directory_names) == 0:
        name = directory_path.split("/")[-1]

        children_directories[name] = {}
        children_directories[name]["path"] = directory_path

for fred_number, value in json_data.items():
    if value in children_directories:
        children_directories[value]['id'] = fred_number

for name, data in children_directories.items():
    obtain_series_data(name, data)
