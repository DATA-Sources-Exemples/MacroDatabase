import requests
import json

LIST_OF_COUNTRY_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/Countries/"
                 "list_of_options.json").text)

LIST_OF_STATES_OPTIONS = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Curated/States/"
                 "list_of_options.json").text)

STATES = json.loads(
    requests.get("https://raw.githubusercontent.com/JerBouma/MacroDatabase/master/Structure/states.json/").text)
