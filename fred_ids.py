import json
import os
import multiprocessing as mp

import requests


def get_fred_id(fred_id):
    r = requests.get(f"https://fred.stlouisfed.org/categories/{fred_id}")

    if "Looking for Something?" not in r.text:
        json.dump("", open(f"IDs/{fred_id}.json", "w"))
        print(f"{fred_id} added")


if __name__ == "__main__":
    if "IDs" not in os.listdir():
        os.mkdir("IDs")

    already_checked = [int(file.strip(".json")) for file in os.listdir("IDs") if ".json" in file]

    fred_ids = set(range(0, 50_000 + 1)) - set(already_checked)

    pool = mp.Pool(mp.cpu_count())
    print(f"Starting CPUs..")
    result = pool.map(get_fred_id, fred_ids)
    print(f"Ready!")


