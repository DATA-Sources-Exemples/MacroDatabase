<p align="center">
  <a href="https://openbb.co/">
    <img src="https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/images/openbb_splashscreen.png" alt="Logo" width="1000">
  </a>
</p>
<h3 align="center">Macro Database 🌎</h3>

It's one thing to understand companies existing in countries, sectors and industries and another to understand 
movements within these categories due to macroeconomics. The former is attempted to be solved with
[FinanceDatabase](https://github.com/JerBouma/FinanceDatabase) and the MacroDatabase is an attempt to cover the latter. 

Within this database of over 570.000 datasets, you are able to view an incredibly large amount of financial indicators 
(e.g. GDP, employment rates, interest & inflation rates), prices (e.g. commodities, CPIs and housing indices), an 
extensive variety of country data (e.g. government bond yields of the Netherlands, real consumption of households 
in Japan) and so much more.

| Category                                | Datasets                      |                 
|:----------------------------------------|------------------------------:|
| Prices                                  | 10,406                        |                       
| U.S. Regional Data                      | 418,232                       |                                         
| Money, Banking, & Finance               | 11,585                        |                                               
| Production & Business Activity          | 3,777                         |                                              
| Academic Data                           | 14,880                        |                    
| National Accounts                       | 12,448                        |                                           
| International Data                      | 95,706                        |                                                 
| Population, Employment, & Labor Markets | 9,077                         |
| **Total**                               | **576,111**                   |

Find an overview of the largest categories within the database [here](/Database). The categorisation comes from 
the [Federal Reserve Economic Data (FRED) database](https://fred.stlouisfed.org/) and this repository aims to 
make sense of all the data within these categories.

## Table of Contents

1. [Using the Database](#using-the-database)
3. [Questions & Answers](#questions--answers)
4. [Contribution](#contribution)

## Using the Database
To access the database you can download the entire repository, but I strongly recommend making use of the package 
closely attached to the database. It allows you to select specific json files as well as search through collected
data with a specific query.

### Installation
You can install the package with the following steps:
1. `pip install macrodatabase`
2. (within Python) `import macrodatabase as md`

### Functions
The package has the following functions:

- `show_country_options(search=None, category=None, parameter=None)` - gives curated country options. If no 
parameter is provided, gives all options. If search is provided, searches with this query and if category or parameter 
is provided, gives a specific selection.
- `show_states_options(search=None, category=None, parameter=None)` - gives curated states options. If no 
parameter is provided, gives all options. If search is provided, searches with this query and if category or parameter 
is provided, gives a specific selection.
- `show_database_options(search=None, include_discontinued=False)` - gives all options within the database given 
a certain search term or all if no search term is provided.
- `select_country_data(category, parameter, country=None, unit=None, period=None, seasonality=True)` - gives a certain 
set of curated country data based on the parameters given. E.g. "GDP" and "Liquid Liabilities to GDP". You can also 
specify the unit, period and seasonality to get specific types of data. If not provided, the function returns all 
types.
- `select_states_data(category, parameter, state=None, unit=None, period=None, seasonality=True)` - gives a certain 
set of curated state data based on the parameters given. E.g. "Real Estate" and "Housing Inventory: Average 
Listing Price". You can also specify the unit, period and seasonality to get specific types of data. If not provided, 
the function returns all types.
- `select_database_data(parameter)` - grab data from the whole database. This follows the structure that can be 
obtained via `show_database_options`. E.g. to select Mortgage Rates you would use 'Interest Rates/Mortgage Rates'.
- `collect_data(ids, api_key, show_progress=True)` - based on IDs, collect data via the 
[FREDAPI](https://github.com/mortada/fredapi) package. This allows you to instantly collect all data for the 
curated list. For example, all countries you can find within 'Liquid Liabilities to GDP' (150+).

## Questions & Answers
In this section you can find answers to commonly asked questions. In case the answer to your question is not here, 
consider creating an [Issue](https://github.com/OpenBB-finance/MacroDatabase/issues).

- **How did you get your data?**
    - Please check the [Methodology](https://github.com/OpenBB-finance/MacroDatabase/tree/master/Methodology).
- **Which countries and states are supported?**
    - Please see [Countries](https://github.com/OpenBB-finance/MacroDatabase/tree/master/Structure/countries.json) and
    [States](https://github.com/OpenBB-finance/MacroDatabase/tree/master/Structure/states.json).
- **How can I find out which options exists?**
    - For this you can use the ``show_country_options`` function for the Curated Countries, ``show_state_options`` 
    for the Curated States and ``show_database_options`` function for general database querying.
- **How frequently does the Database get updated?**
    - Every sunday this database gets refreshed via GitHub Actions.
    See [Methodology](https://github.com/OpenBB-finance/MacroDatabase/tree/master/Methodology) for how this is done.

## Contribution
Projects are bound to have (small) errors and can always be improved. Therefore, we highly encourage you to submit 
issues and create pull requests to improve the package.