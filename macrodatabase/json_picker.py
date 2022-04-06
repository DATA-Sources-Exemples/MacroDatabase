import requests
import json
import pandas as pd

request = requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/"
                       "Curated/Countries/list_of_options.json")
list_of_options = json.loads(request.text)


def select_country_data(category, parameter, country=None, unit=None, period=None, seasonality=True,
                        repo_url="https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Database/"
                                 "_Curated/"):
    """
    Description
    ----
    Returns all cryptocurrencies when no input is given and has the option to give
    a specific set of symbols for the cryptocurrency you provide.

    Input
    ----
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
    json_data (dictionary)
        Returns a dictionary with a selection or all data based on the input.
    """
    if category in list_of_options:
        category_url = category.replace(" ", "%20")
        if parameter in list_of_options[category]:
            parameter_url = parameter.replace(" ", "%20")

            if None in (unit, period):
                combination = parameter_url
                central_bank_path = f"{repo_url}/{category_url}/{parameter_url}/{combination}.json"
            else:
                if seasonality:
                    combination = f"{unit}_{period}_Seasonally Adjusted"
                    if combination not in list_of_options[category][parameter]:
                        if f"{unit}_{period}_Not Seasonally Adjusted" in list_of_options[category][parameter]:
                            combination = f"{unit}_{period}_Not Seasonally Adjusted"
                else:
                    combination = f"{unit}_{period}_Not Seasonally Adjusted"
                    if combination not in list_of_options[category][parameter]:
                        if f"{unit}_{period}_Seasonally Adjusted" in list_of_options[category][parameter]:
                            combination = f"{unit}_{period}_Seasonally Adjusted"

                central_bank_path = f"{repo_url}/{category_url}/{parameter_url}/{combination.replace(' ', '%20')}.json"

            try:
                request = requests.get(central_bank_path)
                json_data = pd.DataFrame.from_dict(json.loads(request.text), orient='index')

                if country:
                    try:
                        json_data = json_data.loc[country]
                    except KeyError as error:
                        error = str(error)
                        print(f"Not able to obtain data for {error[error.find('[') + 1:error.find(']')]}.")

                return json_data
            except json.decoder.JSONDecodeError:
                print(f"Not able to collect data for {parameter} with combination "
                      f"{', '.join(combination.split('_'))}")
        else:
            print(f"Can not find {parameter} within {category}.")
    else:
        print(f"Can not find {category}")
