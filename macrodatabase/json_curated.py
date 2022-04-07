import json

import pandas as pd
import requests

LIST_OF_COUNTRY_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/Countries/"
                 "list_of_options.json").text)

LIST_OF_STATES_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/States/"
                 "list_of_options.json").text)

STATES = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Structure/"
                 "states.json").text)


def select_country_data(category, parameter, country=None, unit=None, period=None, seasonality=True,
                        repo_url="https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/Countries/"):
    """
    Description
    ----
    Select from a range of curated parameters. For example, see the inflation rates of 150 countries by selecting
    category = Inflation and parameter = Inflation, consumer prices. With this information, you can collect the series
    via a variety of FRED data collection packages.

    Input
    ----
    category (string)
        The category you wish to show data for
    parameter (string)
        The parameter you wish to show data for
    country (string or list, default is None):
        The country or countries you wish to show data for
    unit (string, default is None)
        Unit, the type of how data is displayed. E.g. 'Percent'
    period (string, default is None)
        The period, this can be "Annually", "Quarterly" or "Monthly"
    seasonality (boolean, default is True)
        Whether to adjust for seasonality. If this parameter is set to True and it's not available, it will convert
        automatically to False.

    Output
    ----
    df (pd.DataFrame)
        Returns a DataFrame with a selection or all data based on the input.
    """
    if category in LIST_OF_COUNTRY_OPTIONS:
        category_url = category.replace(" ", "%20")
        if parameter in LIST_OF_COUNTRY_OPTIONS[category]:
            parameter_url = parameter.replace(" ", "%20")

            if isinstance(country, str):
                country = [country]
            if country:
                for value in country:
                    if value not in LIST_OF_COUNTRY_OPTIONS[category][parameter][parameter]:
                        country = False
                        print(f"The country {value} is not an option. Therefore, continuing without country slicing.")
                        break

            if None in (unit, period):
                combination = parameter_url
                location = f"{repo_url}/{category_url}/{parameter_url}/{combination}.json"
            else:
                if seasonality:
                    combination = f"{unit}_{period}_Seasonally Adjusted"
                    if combination not in LIST_OF_COUNTRY_OPTIONS[category][parameter]:
                        if f"{unit}_{period}_Not Seasonally Adjusted" in LIST_OF_COUNTRY_OPTIONS[category][parameter]:
                            combination = f"{unit}_{period}_Not Seasonally Adjusted"
                else:
                    combination = f"{unit}_{period}_Not Seasonally Adjusted"
                    if combination not in LIST_OF_COUNTRY_OPTIONS[category][parameter]:
                        if f"{unit}_{period}_Seasonally Adjusted" in LIST_OF_COUNTRY_OPTIONS[category][parameter]:
                            combination = f"{unit}_{period}_Seasonally Adjusted"

                location = f"{repo_url}/{category_url}/{parameter_url}/{combination.replace(' ', '%20')}.json"

            try:
                request = requests.get(location)
                json_data = json.loads(request.text)

                if combination == parameter_url and len(LIST_OF_COUNTRY_OPTIONS[category][parameter]) > 2:
                    df = pd.DataFrame.from_dict(json_data, orient="index").stack().to_frame()
                    df = pd.DataFrame(df[0].values.tolist(), index=df.index)
                else:
                    df = pd.DataFrame.from_dict(json_data, orient='index')

                if country:
                    if isinstance(df.index, pd.MultiIndex):
                        df = df.loc[slice(None), country, :]
                    else:
                        df = df.loc[country]

                return df
            except json.decoder.JSONDecodeError:
                print(f"Not able to collect data for {parameter} with combination "
                      f"{', '.join(combination.split('_'))}")
        else:
            print(f"Can not find '{parameter}' within '{category}'.")
    else:
        print(f"Can not find '{category}'")


def show_country_options(search=None, category=None, parameter=None):
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
    if search:
        search_dict = {}
        for cat in LIST_OF_COUNTRY_OPTIONS:
            for par in LIST_OF_COUNTRY_OPTIONS[cat]:
                if search.lower() in par.lower():
                    if cat not in search_dict:
                        search_dict[cat] = {}
                    search_dict[cat][par] = LIST_OF_COUNTRY_OPTIONS[cat][par]

        return search_dict

    elif category:
        if category not in LIST_OF_COUNTRY_OPTIONS:
            print(f"Can not find '{category}'")
        elif parameter:
            if parameter not in LIST_OF_COUNTRY_OPTIONS[category]:
                print(f"Can not find '{parameter}' within '{category}'.")
            else:
                return LIST_OF_COUNTRY_OPTIONS[category][parameter]
        else:
            return LIST_OF_COUNTRY_OPTIONS[category]
    else:
        return LIST_OF_COUNTRY_OPTIONS


def select_states_data(category, parameter, state=None, unit=None, period=None, seasonality=True,
                       repo_url="https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/States/"):
    """
    Description
    ----
    Select from a range of curated parameters. For example, see the Homeownership Rate of multiple states by selecting
    category = Real Estate and parameter = Homeownership Rate. With this information, you can collect the series
    via a variety of FRED data collection packages.

    Input
    ----
    category (string)
        The category you wish to show data for
    parameter (string)
        The parameter you wish to show data for
    state (string or list, default is None):
        The state or states you wish to show data for
    unit (string, default is None)
        Unit, the type of how data is displayed. E.g. 'Percent'
    period (string, default is None)
        The period, this can be "Annually", "Quarterly" or "Monthly"
    seasonality (boolean, default is True)
        Whether to adjust for seasonality. If this parameter is set to True and it's not available, it will convert
        automatically to False.

    Output
    ----
    df (pd.DataFrame)
        Returns a DataFrame with a selection or all data based on the input.
    """
    if category in LIST_OF_STATES_OPTIONS:
        category_url = category.replace(" ", "%20")
        if parameter in LIST_OF_STATES_OPTIONS[category]:
            parameter_url = parameter.replace(" ", "%20")

            if isinstance(state, str):
                state = [state]
            if state:
                for value in state:
                    if value not in LIST_OF_STATES_OPTIONS[category][parameter][parameter]:
                        state = False
                        print(f"The state {value} is not an option. Therefore, continuing without state slicing.")
                        break

            if None in (unit, period):
                combination = parameter_url
                location = f"{repo_url}/{category_url}/{parameter_url}/{combination}.json"
            else:
                if seasonality:
                    combination = f"{unit}_{period}_Seasonally Adjusted"
                    if combination not in LIST_OF_STATES_OPTIONS[category][parameter]:
                        if f"{unit}_{period}_Not Seasonally Adjusted" in LIST_OF_STATES_OPTIONS[category][parameter]:
                            combination = f"{unit}_{period}_Not Seasonally Adjusted"
                else:
                    combination = f"{unit}_{period}_Not Seasonally Adjusted"
                    if combination not in LIST_OF_STATES_OPTIONS[category][parameter]:
                        if f"{unit}_{period}_Seasonally Adjusted" in LIST_OF_STATES_OPTIONS[category][parameter]:
                            combination = f"{unit}_{period}_Seasonally Adjusted"

                location = f"{repo_url}/{category_url}/{parameter_url}/{combination.replace(' ', '%20')}.json"

            try:
                request = requests.get(location)
                json_data = json.loads(request.text)

                if combination == parameter_url and len(LIST_OF_STATES_OPTIONS[category][parameter]) > 2:
                    df = pd.DataFrame.from_dict(json_data, orient="index").stack().to_frame()
                    df = pd.DataFrame(df[0].values.tolist(), index=df.index)
                else:
                    df = pd.DataFrame.from_dict(json_data, orient='index')

                if state:
                    if isinstance(df.index, pd.MultiIndex):
                        df = df.loc[slice(None), state, :]
                    else:
                        df = df.loc[state]

                return df
            except json.decoder.JSONDecodeError:
                print(f"Not able to collect data for {parameter} with combination "
                      f"{', '.join(combination.split('_'))}")
        else:
            print(f"Can not find '{parameter}' within '{category}'.")
    else:
        print(f"Can not find '{category}'")


def show_states_options(search=None, category=None, parameter=None):
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
    LIST_OF_STATES_OPTIONS (Dictionary)
        Returns a dictionary with a selection or all available options based on the input.
    """
    if search:
        search_dict = {}
        for cat in LIST_OF_STATES_OPTIONS:
            for par in LIST_OF_STATES_OPTIONS[cat]:
                if search.lower() in par.lower():
                    if cat not in search_dict:
                        search_dict[cat] = {}
                    search_dict[cat][par] = LIST_OF_STATES_OPTIONS[cat][par]

        return search_dict

    elif category:
        if category not in LIST_OF_STATES_OPTIONS:
            print(f"Can not find '{category}'")
        elif parameter:
            if parameter not in LIST_OF_STATES_OPTIONS[category]:
                print(f"Can not find '{parameter}' within '{category}'.")
            else:
                return LIST_OF_STATES_OPTIONS[category][parameter]
        else:
            return LIST_OF_STATES_OPTIONS[category]
    else:
        return LIST_OF_STATES_OPTIONS
