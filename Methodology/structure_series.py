import json
import os

from natsort import natsorted

try:
    path_str = "Database"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"

children_directories = {}

for directory_path, directory_names, _ in os.walk(path_str):
    if directory_path.split("/")[-1] == "Discontinued":
        directory_path = "/".join(directory_path.split("/")[:-1])

    name = directory_path.split("/")[-1]

    all_json_files = dict()
    all_discontinued_json_files = dict()
    all_json_files_including_discontinued = dict()

    all_json_name = f"_{name}.json"
    all_discontinued_name = f"_{name}_Discontinued.json"
    all_json_and_discontinued_name = f"_{name}_Incl_Discontinued.json"

    if all_json_name in os.listdir(directory_path):
        os.remove(f"{directory_path}/{all_json_name}")
    if all_json_and_discontinued_name in os.listdir(directory_path):
        os.remove(f"{directory_path}/{all_json_and_discontinued_name}")

    if "Discontinued" in os.listdir(directory_path):
        if all_discontinued_name in os.listdir(f"{directory_path}/Discontinued"):
            os.remove(f"{directory_path}/Discontinued/{all_discontinued_name}")

    print(f"Creating structure for {name} ({directory_path})")

    if "Discontinued" in os.listdir(directory_path):
        include_discontinued = True
    else:
        include_discontinued = False

    for file in os.listdir(directory_path):
        if file == "Discontinued" and include_discontinued:
            discontinued_path = f"{directory_path}/Discontinued"
            for discontinued_file in os.listdir(discontinued_path):
                if ".json" in discontinued_file:
                    file_name = discontinued_file.strip('.json')
                    all_json_files_including_discontinued[file_name] = json.load(open(
                        f"{discontinued_path}/{discontinued_file}", "r"))
                    all_json_files_including_discontinued[file_name]['path'] = directory_path
                    all_discontinued_json_files[file_name] = all_json_files_including_discontinued[file_name]
        if ".json" in file and file != "ID.json":
            file_name = file.strip('.json')
            all_json_files[file_name] = json.load(open(
                f"{directory_path}/{file}", "r"))
            all_json_files[file_name]['path'] = directory_path
            all_json_files_including_discontinued[file_name] = all_json_files[file_name]

    natural_sort = natsorted(all_json_files)
    all_json_files_sorted = {}

    for number in natural_sort:
        all_json_files_sorted[number] = all_json_files[number]

    if all_json_files_sorted:
        json.dump(all_json_files_sorted, open(f"{directory_path}/{all_json_name}", "w"), indent=2)

    if include_discontinued:
        natural_sort = natsorted(all_discontinued_json_files)
        all_discontinued_json_files_sorted = {}

        for number in natural_sort:
            all_discontinued_json_files_sorted[number] = all_discontinued_json_files[number]

        if all_discontinued_json_files_sorted:
            json.dump(all_discontinued_json_files_sorted, open(
                f"{directory_path}/Discontinued/{all_discontinued_name}", "w"), indent=2)

        natural_sort = natsorted(all_json_files_including_discontinued)
        all_json_files_including_discontinued_sorted = {}

        for number in natural_sort:
            all_json_files_including_discontinued_sorted[number] = all_json_files_including_discontinued[number]

        if all_json_files_including_discontinued_sorted:
            json.dump(all_json_files_including_discontinued_sorted, open(
                f"{directory_path}/{all_json_and_discontinued_name}", "w"), indent=2)

print("Done!")
