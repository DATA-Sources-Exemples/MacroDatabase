The following files are used in this exact order to create the database:
1. **find_fred_ids.py**: to be able to determine which FRED IDs actually exists, this file is used to register the working IDs. This also prevents unnecessary calls to the FRED database.
2. **create_folders.py**: each FRED ID's data, that is found within the 'IDs' folder, is collected and the 'parent' categories and further are determined. This leads to the structure that the Database has.
3. **obtain_series.py**: by finding the deepest layers of the database structure, it can be determined which folder requires a search for series (data).
4. **structure_series.py**: structures the series in such a way that you are able to obtain "overview" files (with or without discontinued series). E.g. "_United States.json" contains all json files from Database/International Data/Countries/United States.
5. **perform_countries_curation.py**: curate information about countries for easy comparison between each country. For example by looking at inflation rates or GDP.
6. **perform_states_curation.py**: curate information about states in the United States for easy comparison between each state. For example by looking at Home ownership.

Within the repository, an automatic script is run every sunday that deletes and then re-collects the series. This is to 
ensure that the information remains up to date and potentially removed series by FRED are removed and discontinued 
series are moved to the corresponding folder.