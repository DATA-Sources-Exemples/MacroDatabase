import os
from tabulate import tabulate
import pandas as pd
import json

try:
    path_str = "Database"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"


# Create table overview (categories, sub-categories and files)
table_structure = {}

for top_level in os.listdir(path_str):
    if top_level in ['.DS_Store', "README.md"]:
        continue

    table_structure[top_level] = {}
    path_secondary = f"{path_str}/{top_level}"

    for secondary_level in os.listdir(path_secondary):
        if secondary_level in ['.DS_Store', "README.md"]:
            continue

        amount_of_files = 0
        for directory_path, directory_names, directory_files in os.walk(f"{path_secondary}/{secondary_level}"):
            if len(directory_names) == 0 or len(directory_names) == 1 and directory_names[0] == "Discontinued":
                for file in directory_files:
                    if ".json" in file:
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

overview = tabulate(
    df_print, tablefmt="github", headers=['Category', "Sub-Category", "Files"],
    colalign=("left", "left", "right"), showindex=False)

# Create README files for one layer above the folders containing json files
for directory_path, directory_names, _ in os.walk(path_str):
    # create_readme = False
    #
    # for folder in directory_names:
    #     for file in os.listdir(f"{directory_path}/{folder}"):
    #         if '.json' in file:
    #             create_readme = True
    #             break
    #     if create_readme:
    #         break

    # if create_readme:
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
for directory_path, directory_names, _ in os.walk(path_str):
    if len(directory_names) == 0:
        if directory_path.split("/")[-1] == "Discontinued":
            directory_path = "/".join(directory_path.split("/")[:-1])

        name = directory_path.split("/")[-1]
        all_json_name = f"_{name}.json"

        print(f"Creating Series README for {name} ({directory_path})")

        all_json_data = json.load(open(f"{directory_path}/{all_json_name}", "r"))

        if all_json_data:
            df = pd.DataFrame.from_dict(all_json_data, orient='index')[
                ['id', 'title', 'observation_start', 'observation_end']]
            markdown = df.to_markdown(tablefmt="github", index=False)

            with open(f"{directory_path}/README.md", "w") as file:
                file.write(markdown)
