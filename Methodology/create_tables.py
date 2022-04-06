import json
import os

import pandas as pd

try:
    path_str = "Database"
    curation_countries_str = "Curated/Countries"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"
    curation_countries_str = "../Curated/Countries"

for table_location in [path_str]:
    # Create README files for all locations to count folders and files
    for directory_path, directory_names, _ in os.walk(table_location):
        name = directory_path.split("/")[-1]
        print(f"Creating Folder README for {name} ({directory_path})")
        folder_structure = pd.DataFrame(columns=['Folder', 'Files / Folders'])

        for folder in directory_names:
            files = os.listdir(f"{directory_path}/{folder}")
            json_file_count = len([file for file in files if '.json' in file])
            folder_count = len([file for file in files if '.json' not in file and "README.md" not in file])

            if folder_count > 1:
                folder_df = pd.DataFrame([[folder, folder_count]], columns=folder_structure.columns)
            else:
                folder_df = pd.DataFrame([[folder, json_file_count]], columns=folder_structure.columns)

            folder_structure = pd.concat([folder_structure, folder_df])

        markdown = folder_structure.to_markdown(tablefmt="github", index=False)

        with open(f"{directory_path}/README.md", "w") as file:
            file.write(markdown)

    # Create README files for subpages
    for directory_path, directory_names, _ in os.walk(table_location):
        if directory_path.split("/")[-1] == "Discontinued":
            paths = directory_path, "/".join(directory_path.split("/")[:-1])
        else:
            paths = None, directory_path

        for path in paths:
            if path:
                name = paths[1].split("/")[-1]

                if 'Discontinued' in path:
                    all_json_name = f"_{name}_Discontinued.json"
                else:
                    all_json_name = f"_{name}.json"

                print(f"Creating Series README for {name} ({path})")

                all_json_data = json.load(open(f"{path}/{all_json_name}", "r"))

                if all_json_data:
                    df = pd.DataFrame.from_dict(all_json_data, orient='index')
                    if 'title' in df:
                        df = df[['id', 'title', 'observation_start', 'observation_end']]
                        markdown = df.to_markdown(tablefmt="github", index=False)

                        with open(f"{path}/README.md", "w") as file:
                            file.write(markdown)

    # Create table overview (categories, sub-categories and files) in the main folder
    table_structure = {}

    print(f"Creating Overview README in {table_location}")
    for top_level in os.listdir(table_location):
        if top_level in ['.DS_Store', "README.md", "_Database.json"]:
            continue

        table_structure[top_level] = {}
        path_secondary = f"{table_location}/{top_level}"

        for secondary_level in os.listdir(path_secondary):
            if secondary_level in ['.DS_Store', "README.md", "ID.json", f"_{secondary_level}.json"]:
                continue

            amount_of_files = 0
            for directory_path, directory_names, directory_files in os.walk(f"{path_secondary}/{secondary_level}"):
                if len(directory_names) == 0 or len(directory_names) == 1 and directory_names[0] == "Discontinued":
                    for file in directory_files:
                        if ".json" in file and file != "ID.json":
                            amount_of_files += 1

            table_structure[top_level][secondary_level] = amount_of_files

    reform = {(outerKey, innerKey): values for outerKey, innerDict in table_structure.items()
              for innerKey, values in innerDict.items()}
    df = pd.DataFrame.from_dict(reform, orient='index')
    df.index = pd.MultiIndex.from_tuples(df.index)

    df_print = df.reset_index()
    prev_level = [None] * df.index.nlevels
    for irow, (idx, row) in enumerate(df.iterrows()):
        for ilevel, level in enumerate(idx):
            if prev_level[ilevel] == level:
                df_print.iat[irow, ilevel] = ''
            prev_level[ilevel] = level

    df_print[0] = df_print[0].apply(lambda x: "{:,}".format(x).rjust(15))
    df_print.columns = ['Category', "Sub-Category", "Files"]

    markdown = df_print.to_markdown(tablefmt="github", index=False)

    with open(f"{table_location}/README.md", "w") as file:
        file.write(markdown)
