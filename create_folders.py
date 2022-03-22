import json
import os
import time

import fred

from config import misc, RESET


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
                try:
                    category_parent = fred.categories(category_parent['categories'][0]['parent_id'])

                    id = category_parent['categories'][0]['id']
                    name = category_parent['categories'][0]['name']

                    parents_names.insert(0, name)

                    json.dump(name, open(f"IDs/{id}.json", "w"))
                except KeyError as error:
                    return print(f"An error ocurred {error} for FRED ID {id}")

            folder = "Data/"
            for parent in parents_names:
                if parent not in os.listdir(folder):
                    try:
                        os.mkdir(f"{folder}/{parent}")

                        with open(f"{folder}/{parent}/README.md", mode='a'):
                            pass

                    except FileNotFoundError:
                        return print(f"The folder {folder}/{parent} does not exist yet.")

                folder += f"{parent}/"


if RESET:
    print(f"RESET is set to {RESET} thus emptying all IDs")
    for file in os.listdir("IDs"):
        if file == "_IDs.json":
            os.remove(f"IDs/{file}")
        else:
            json.dump("", open(f"IDs/{file}", "w"))

fred.key(misc[214][43:75])
if "Data" not in os.listdir():
    os.mkdir("Data")

fred_ids = [int(file.strip(".json")) for file in os.listdir("IDs") if ".json" in file and "_IDs.json" not in file][:15]

for fred_id in fred_ids:
    get_fred_data(fred_id)
