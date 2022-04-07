import pandas as pd
from fredapi import Fred
from tqdm import tqdm


def collect_data(ids, api_key, show_progress=True):
    """
    Description
    ----
    Select from a range of curated parameters. For example, see the inflation rates of 150 countries by selecting
    category = Inflation and parameter = Inflation, consumer prices. With this information, you can collect the series
    via a variety of FRED data collection packages.

    Input
    ----
    ids (list)
        The ids you wish to collect data for.
    api_key (string)
    package_type (string, default is 'fred')
        You are able to obtain the data via two packages, 'fred' and 'fredapi':
            - fred: https://github.com/zachwill/fred
            - fredapi: https://github.com/mortada/fredapi

    Output
    ----
    df (pd.DataFrame)
        Returns a DataFrame with a selection or all data based on the input.
    """
    dataset = {}
    data_errors = []
    fred = Fred(api_key=api_key)

    if isinstance(ids, str):
        ids = [ids]

    if show_progress:
        for series_id in tqdm(ids, desc="Collecting data"):
            try:
                dataset[series_id] = fred.get_series(series_id)
            except ValueError:
                data_errors.append(series_id)
    else:
        for series_id in ids:
            try:
                dataset[series_id] = fred.get_series(series_id)
            except ValueError:
                data_errors.append(series_id)

    df = pd.DataFrame.from_dict(dataset)

    if data_errors:
        print(f"Was not able to retrieve data for: {', '.join(data_errors)}")

    return df
