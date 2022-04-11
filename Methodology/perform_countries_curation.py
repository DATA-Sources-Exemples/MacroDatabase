import json
import os
import shutil

from tqdm import tqdm

RESET = True

try:
    path_str = "Database"
    structure_str = "Structure"
    curated_str = "Curated/Countries"
    base_directory = "."
    os.listdir("Database")
except FileNotFoundError:
    path_str = "../Database"
    structure_str = "../Structure"
    curated_str = "../Curated/Countries"
    base_directory = "../"

if RESET:
    if "Curated" in os.listdir(base_directory):
        if "Countries" in os.listdir(f"{base_directory}/Curated"):
            shutil.rmtree(f"{base_directory}/Curated/Countries")
if "Curated" not in os.listdir(base_directory):
    os.mkdir(f"{base_directory}/Curated")
if "Countries" not in os.listdir(f"{base_directory}/Curated"):
    os.mkdir(f"{base_directory}/Curated/Countries")

COUNTRIES = json.load(open(f"{structure_str}/countries.json", "r"))
CURATION_LIST = json.load(open(f"{structure_str}/country_curation_list.json", "r"))

similarities = {}
dataset = {}
previous_item = None
previous_text = None
previous_unit = None
previous_frequency = None
previous_seasonal_adjustment = None

for country in COUNTRIES:
    dataset[country] = json.load(open(f"{path_str}/International Data/Countries/{country}/_{country}.json", "r"))

# Create country macro data
for country_1 in tqdm(dataset, desc="Collecting country options"):
    for key_1, value_1 in dataset[country_1].items():
        title_1 = value_1['title']

        if f"for the {country_1}" in title_1 or f"for {country_1}" in title_1 or f"in {country_1}" in title_1:
            if f"for the {country_1}" in title_1:
                item_1 = title_1.split(f" for the {country_1}")[0]
            elif f"for {country_1}" in title_1:
                item_1 = title_1.split(f" for {country_1}")[0]
            else:
                item_1 = title_1.split(f" in {country_1}")[0]

            units_1 = value_1['units']
            frequency_1 = value_1['frequency']
            seasonal_adjustment_1 = value_1['seasonal_adjustment']

            previous_text = f"{item_1} ({units_1}, {frequency_1}, {seasonal_adjustment_1})"
            previous_item = item_1
            previous_unit = units_1
            previous_frequency = frequency_1
            previous_seasonal_adjustment = seasonal_adjustment_1

            if item_1 not in similarities:
                similarities[item_1] = {}

            name = f"{units_1}_{frequency_1}_{seasonal_adjustment_1}"
            similarities[item_1][name] = {country_1: value_1}

            for country_2 in dataset:
                if country_2 == country_1:
                    continue

                for key_2, value_2 in dataset[country_2].items():
                    title_2 = value_2['title']

                    if f"for the {country_2}" in title_2:
                        item_2 = title_2.split(f" for the {country_2}")[0]
                    elif f"for {country_2}" in title_2:
                        item_2 = title_2.split(f" for {country_2}")[0]
                    else:
                        item_2 = title_2.split(f" in {country_2}")[0]

                    if item_1 == item_2:
                        units_2 = value_2['units']
                        frequency_2 = value_2['frequency']
                        seasonal_adjustment_2 = value_2['seasonal_adjustment']

                        similarities[item_1][name][country_2] = value_2

# Obtain Academic Data JSON files:
json_structure = json.load(open(f"{structure_str}/database_structure.json", "r"))

academic_data = []
for path in json_structure:
    if "Academic Data" in path:
        folder = path.split("/")[-1]

        try:
            aggregated_json = json.load(open(f"{path}/_{folder}.json", "r"))
        except FileNotFoundError:
            try:
                aggregated_json = json.load(open(f"{path[3:]}/_{folder}.json", "r"))
            except FileNotFoundError:
                aggregated_json = {}
                print(f"Not able to obtain Academic Data for {folder}")

        for key, data in aggregated_json.items():
            if "title" in data:
                academic_data.append(data['title'])

for key in academic_data:
    similarities.pop(key, None)

# Clean up the data and add categorization
skip = ["Use of Financial Services", "Geographical Outreach"]
similarities_updated = {}
for value in similarities:
    dictionary = {}

    if ":" in value and value.count(":") > 1 or any(x in value for x in skip):
        dict_layers = value.split(":")

        if any(x in value for x in skip):
            last_layer = dict_layers[-1].strip()
        else:
            last_layer = f"{dict_layers[0].strip()} {dict_layers[-1].strip()}"

        similarities_updated[last_layer] = similarities[value]
    else:
        similarities_updated[value] = similarities[value]

# Perform curation
curated = {key: {} for key in CURATION_LIST.keys()}
curated['Undefined'] = {}
for key, data in similarities_updated.items():
    category_decision = "Undefined"

    for title, curation_values in CURATION_LIST.items():
        if "GDP" in key:
            curated["GDP"][key] = data
            category_decision = title
        elif category_decision == "Undefined":
            for value in curation_values:
                if value.lower() in key.lower():
                    curated[title][key] = data
                    category_decision = title
                    continue

    if category_decision == "Undefined":
        curated["Undefined"][key] = data

# Create curated folder structure
list_of_options = {}
for key_1, values_1 in curated.items():
    if key_1 not in os.listdir(f"{curated_str}"):
        os.mkdir(f"{curated_str}/{key_1}")
    if key_1 not in list_of_options:
        list_of_options[key_1] = {}

    for key_2, values_2 in values_1.items():
        key_2 = key_2.replace("/", " ")

        if key_2 not in list_of_options[key_1]:
            list_of_options[key_1][key_2] = {key_2: []}

        if key_2 not in os.listdir(f"{curated_str}/{key_1}"):
            try:
                os.mkdir(f"{curated_str}/{key_1}/{key_2}")
            except FileExistsError as error:
                print(f"Folder already exists for {str(key_2)}")

        general_dict = {}

        for key_3, values_3 in values_2.items():
            if key_3 not in general_dict:
                general_dict[key_3] = {}
            if key_3 not in list_of_options[key_1][key_2]:
                list_of_options[key_1][key_2][key_3] = []

            json.dump(values_2[key_3], open(f"{curated_str}/{key_1}/{key_2}/{key_3}.json", "w"), indent=2)

            for key_4, values_4 in values_3.items():
                if key_4 not in list_of_options[key_1][key_2][key_2]:
                    list_of_options[key_1][key_2][key_2].append(key_4)
                if key_4 not in list_of_options[key_1][key_2][key_3]:
                    list_of_options[key_1][key_2][key_3].append(key_4)

                general_dict[key_3][key_4] = values_4

        keys = list(general_dict.keys())

        if len(keys) == 1:
            json.dump(general_dict[keys[0]], open(f"{curated_str}/{key_1}/{key_2}/{key_2}.json", "w"), indent=2)
        else:
            json.dump(general_dict, open(f"{curated_str}/{key_1}/{key_2}/{key_2}.json", "w"), indent=2)

# Export list of options
json.dump(list_of_options, open(f"{curated_str}/list_of_options.json", "w"), indent=2)
