import json
import os
import time

import fred

API_KEY = "6fa40707f1690bbcf91356c2ba07dab5"


def get_fred_data(fred_id):

    json_file = json.load(open(f"IDs/{fred_id}.json", "r"))

    if json_file:
        return print(f"FRED ID {fred_id} already acquired")
    else:
        print(f"Attempting Fred ID {fred_id}")

        counter = 0
        category = fred.categories(fred_id)

        if 'error_message' in category.keys():
            error_message = category['error_message']

            if error_message == 'Too Many Requests.  Exceeded Rate Limit':
                print("Too many requests. Waiting..")
                while error_message == 'Too Many Requests.  Exceeded Rate Limit':
                    time.sleep(70)
                    category = fred.categories(fred_id)
                    counter += 1

                    if "error_message" in category.keys():
                        error_message = category['error_message']

                    if counter == 6:
                        counter = 0
                        print(f"Still waiting for FRED id {fred_id}")
            elif error_message == 'Bad Request.  The category does not exist.':
                return print(f"The category {fred_id} does not exist.")

        id = category['categories'][0]['id']
        name = category['categories'][0]['name']
        parent_id = category['categories'][0]['parent_id']
        json.dump(name, open(f"IDs/{fred_id}.json", "w"))

        if parent_id == 0 and name not in category:
            print(f"Skipping {name}")
        else:
            data_names = [x[0] for x in os.walk("Data")]

            for x in data_names:
                split_list = x.split("/")

                if name in split_list:
                    return print(f"{name} ({id}) already collected.")

            parents_names = [name]
            category_parent = category

            while category_parent['categories'][0]['parent_id'] != 0:
                category_parent = fred.categories(category_parent['categories'][0]['parent_id'])

                id = category['categories'][0]['id']
                name = category_parent['categories'][0]['name']

                parents_names.insert(0, name)

                json.dump(name, open(f"IDs/{id}.json", "w"))

            folder = "Data/"
            for parent in parents_names:
                if parent not in os.listdir(folder):
                    try:
                        os.mkdir(f"{folder}/{parent}")
                    except FileNotFoundError:
                        return print(f"The folder {folder}/{parent} does not exist yet.")

                folder += f"{parent}/"


def obtain_series_data(child):
    print(f"Attempting {child['name']} ({child['id']})..")
    fred_id = child['id']
    children = fred.category_series(fred_id)['seriess']

    if "Discontinued" not in os.listdir(child['path']):
        os.mkdir(f"{child['path']}/Discontinued")

    for series in children:
        if "DISCONTINUED" in series['title']:
            path = f"{child['path']}/Discontinued/{series['id']}.json"
        else:
            path = f"{child['path']}/{series['id']}.json"

        json.dump(series, open(path, "w"))
        print(f"Collecties {series} for {child['name']}")


if __name__ == "__main__":
    fred.key(API_KEY)
    fred_ids = [int(file.strip(".json")) for file in os.listdir("IDs") if ".json" in file]

    for fred_id in fred_ids:
        get_fred_data(fred_id)

    json_data = {}
    for file in os.listdir("IDs"):
        if file == "_IDs.json":
            continue
        json_data[file.strip(".json")] = json.load(open(f"IDs/{file}", "r"))
    json.dump(json_data, open(f"IDs/_IDs.json", "w"))

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

    for child in children_directories:
        obtain_series_data(child)
