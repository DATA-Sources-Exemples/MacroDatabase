import os
from tabulate import tabulate
import pandas as pd

try:
    path_str = "Database"
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"


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

print(tabulate(
    df_print, tablefmt="github", headers=['Category', "Sub-Category", "Files"],
    colalign=("left", "left", "right"), showindex=False))
