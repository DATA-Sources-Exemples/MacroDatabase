import json
import os
import time

from natsort import natsorted
import sys

import fred

DELETE_JSON = True

try:
    path_str = "Database/"
    id_str = "IDs/"
    base_directory = "."
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database/"
    id_str = "../IDs/"
    base_directory = "../"

try:
    from config import API_KEYS
except ModuleNotFoundError:
    API_KEYS = False


def obtain_series_data(dictionary):
    name = dictionary[0]
    data = dictionary[1]
    key_counter = 1

    try:
        print(f"Attempting {name} ({data['id']})")
        fred_id = data['id']
    except KeyError:
        return print(f"Not able to get data for {name}")

    try:
        children = fred.category_series(fred_id)
    except json.decoder.JSONDecodeError:
        return print(f"Not able to get data for {name} ({data['id']}")

    if 'error_message' in children.keys():
        error_message = children['error_message']

        if error_message == 'Too Many Requests.  Exceeded Rate Limit':
            print("Too many requests.. waiting..")
            while error_message == 'Too Many Requests.  Exceeded Rate Limit':
                if API_KEYS:
                    fred.key(API_KEYS[key_counter])
                    children = fred.category_series(fred_id)

                    if "error_message" in children.keys():
                        error_message = children['error_message']
                    else:
                        error_message = None

                    key_counter += 1

                    if key_counter == 7:
                        key_counter = 0
                else:
                    time.sleep(65)
                    children = fred.category_series(fred_id)

                    if "error_message" in children.keys():
                        error_message = children['error_message']
                    else:
                        error_message = None

    elif children['seriess']:
        children = children['seriess']

        if "Discontinued" not in os.listdir(data['path']):
            os.mkdir(f"{data['path']}/Discontinued")

        for series in children:
            if "DISCONTINUED" in series['title']:
                path = f"{data['path']}/Discontinued/{series['id']}.json"
            else:
                path = f"{data['path']}/{series['id']}.json"

            json.dump(series, open(path, "w"), indent=2)
    else:
        return print(f"Seriess is empty ({children['seriess']}) for {name} ({data['id']}")


if __name__ == "__main__":
    SUPER_SECRET = sys.argv[1]

    if DELETE_JSON:
        print(f"Because DELETE_JSON is set to {DELETE_JSON}, removing all JSON files within the Database.")
        for directory_path, directory_names, directory_files in os.walk(path_str):
            if len(directory_names) == 0 or len(directory_names) == 1 and directory_names[0] == "Discontinued":
                print(f"Removing JSON files from {directory_path}")
                for file in directory_files:
                    if ".json" in file and file is not "ID.json":
                        os.remove(f"{directory_path}/{file}")

                with open(f"{directory_path}/README.md", mode='a'):
                    pass

    json_data = {}
    fred.key(SUPER_SECRET)
    for file in os.listdir(id_str):
        if file == "_IDs.json" or file == "Bad Request":
            continue
        json_data[file.strip(".json")] = json.load(open(f"{id_str}/{file}", "r"))

    json_data_sorted = {}
    natural_sort = natsorted(json_data)

    for number in natural_sort:
        json_data_sorted[number] = json_data[number]
    json.dump(json_data_sorted, open(f"{id_str}/_IDs.json", "w"), indent=2)

    children_directories = {}

    for directory_path, directory_names, _ in os.walk(path_str):
        if directory_path.split("/")[-1] == "Discontinued":
            directory_path = "/".join(directory_path.split("/")[:-1])

        name = directory_path.split("/")[-1]
        children_directories[name] = {}
        children_directories[name]["path"] = directory_path

    for fred_number, value in json_data.items():
        if value:
            category_id = value['id']
            name = value['name']

            if name in children_directories:
                children_directories[name]['id'] = fred_number

    for child, data in children_directories.items():
        obtain_series_data((child, data))

    print("All done!")
