import json
import multiprocessing as mp
import os
import shutil
import time

import fred

from config import API_KEYS

RESET = True

try:
    path_str = "Database/"
    id_str = "IDs/"
    base_directory = "."
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database/"
    id_str = "../IDs/"
    base_directory = "../"


def get_fred_data(fred_id):
    fred.key(API_KEYS[int(mp.current_process().name[-1]) - 1])
    json_file = json.load(open(f"{id_str}/{fred_id}.json", "r"))

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
                    else:
                        error_message = None

                    if counter == 6:
                        counter = 0
                        print(f"Still waiting for FRED id {fred_id}")
            elif error_message == 'Bad Request.  The category does not exist.':
                if "Bad Request" not in os.listdir(id_str):
                    os.mkdir(f"{id_str}/Bad Request")
                json.dump(error_message, open(f"{id_str}/Bad Request/{fred_id}.json", "w"))
                return print(f"The category {fred_id} does not exist.")

        category_id = category['categories'][0]['id']
        name = category['categories'][0]['name']
        parent_id = category['categories'][0]['parent_id']

        json.dump({'name': name, 'id': category_id}, open(f"{id_str}/{category_id}.json", "w"))

        if parent_id == 0 and name not in category:
            print(f"Skipping {name}")
        else:
            data_names = [x[0] for x in os.walk(path_str)]

            for x in data_names:
                split_list = x.split("/")

                if name in split_list:
                    directory_id = json.load(open(f"{x}/ID.json", "r"))

                    if category_id == directory_id:
                        json.dump({'name': name, 'id': category_id}, open(f"{id_str}/{category_id}.json", "w"))
                        return print(f"{name} ({category_id}) already collected.")

            parents_names = [name]
            parents_ids = [category_id]
            category_parent = category

            while category_parent['categories'][0]['parent_id'] != 0:
                try:
                    category_parent = fred.categories(category_parent['categories'][0]['parent_id'])

                    category_id = category_parent['categories'][0]['id']
                    name = category_parent['categories'][0]['name']

                    parents_names.insert(0, name)
                    parents_ids.insert(0, category_id)

                    json.dump({'name': name, 'id': category_id}, open(f"{id_str}/{category_id}.json", "w"))
                except KeyError as error:
                    return print(f"An error occurred {error} for FRED ID {category_id}")

            folder = path_str
            for parent in zip(parents_names, parents_ids):
                parent_name = parent[0]
                parent_name = parent_name.replace("/", " - ")

                parent_id = parent[1]

                if parent_name not in os.listdir(folder):
                    try:
                        os.mkdir(f"{folder}/{parent_name}")

                        json.dump({"name": parent_name, "id": parent_id}, open(f"{folder}/{parent_name}/ID.json", "w"))

                        with open(f"{folder}/{parent_name}/README.md", mode='a'):
                            pass

                    except FileNotFoundError:
                        return print(f"The folder {folder}/{parent_name} does not exist yet.")
                    except FileExistsError:
                        return print(f"The folder {folder}/{parent_name} already exists.")

                folder += f"{parent_name}/"


def activate_get_fred_data():
    pool = mp.Pool(8)
    result = pool.map(get_fred_data, fred_ids)


if __name__ == "__main__":
    if RESET:
        print(f"RESET is set to {RESET} thus emptying all IDs")
        for file in os.listdir(id_str):
            if file == "_IDs.json":
                os.remove(f"{id_str}/{file}")
            elif file == "Bad Request":
                shutil.rmtree(f"{id_str}/{file}")
            else:
                json.dump("", open(f"{id_str}/{file}", "w"))

    if "Database" not in os.listdir(base_directory):
        os.mkdir("Database")

    fred_ids = [int(file.strip(".json")) for file in os.listdir(id_str) if ".json" in file and "_IDs.json" not in file]

    activate_get_fred_data()
