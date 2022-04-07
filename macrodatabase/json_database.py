import json

import pandas as pd
import requests

LIST_OF_DATABASE_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Structure/"
                 "directory_structure.json").text)

LIST_OF_DATABASE_DISCONTINUED_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Structure/"
                 "directory_discontinued_structure.json").text)


def select_database_data(parameter, repo_url="https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Database/"):
    """
    Description
    ----
    Obtain data from the entire database. For example, obtain all Commodity Prices by setting the parameter equal to
    'Prices/Commodities'. For the usage of this, please use the function show_database_options.

    Input
    ----
    parameter (string)
        The parameter you wish to show data for

    Output
    ----
    df (pd.DataFrame)
        Returns a DataFrame with a selection or all data based on the input.
    """
    if parameter in LIST_OF_DATABASE_OPTIONS or parameter in LIST_OF_DATABASE_DISCONTINUED_OPTIONS:
        if parameter in LIST_OF_DATABASE_DISCONTINUED_OPTIONS:
            path = LIST_OF_DATABASE_DISCONTINUED_OPTIONS[parameter]
        else:
            path = LIST_OF_DATABASE_OPTIONS[parameter]

        path_url = path.replace(" ", "%20")
        location = f"{repo_url}{path_url}"

        try:
            request = requests.get(location)
            json_data = json.loads(request.text)
            df = pd.DataFrame.from_dict(json_data, orient='index')

            return df
        except json.decoder.JSONDecodeError:
            print(f"Not able to collect data for {parameter}.")
    else:
        print(f"Can not find '{parameter}'")


def show_database_options(search=None, include_discontinued=False):
    """
    Description
    ----
    This function returns information about the available options in certain categories and parameters.

    Input
    ----
    category (string, default is None)
        The category you wish to show options for
    parameter (string, default is None)
        The parameter you wish to show options for

    Output
    ----
    LIST_OF_OPTIONS (Dictionary)
        Returns a dictionary with a selection or all available options based on the input.
    """
    search_dict = {}

    for parameter in LIST_OF_DATABASE_OPTIONS:
        if search.lower() in parameter.lower():
            search_dict[parameter] = LIST_OF_DATABASE_OPTIONS[parameter]

    if include_discontinued:
        for parameter in LIST_OF_DATABASE_DISCONTINUED_OPTIONS:
            if search.lower() in parameter.lower():
                search_dict[parameter] = LIST_OF_DATABASE_DISCONTINUED_OPTIONS[parameter]

    df = pd.Series.from_dict(search_dict)

    return df
