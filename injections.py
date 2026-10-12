# "injections.py" from TigerDine-Supplemental-API
# Copyright (c) 2026 NinjaCheetah/Campbell Bagley
# https://github.com/NinjaCheetah/TigerDine-Supplemental-API
#
# Functions to inject local data into the responses from the TigerCenter API.

import json


def inject_const_location_info(data: dict) -> dict:
    const_location_info_raw = open("data/const_location_info.json", "r").read()
    const_location_info = json.loads(const_location_info_raw)

    for location in data["locations"]:
        if location["name"] in const_location_info.keys():
            print("applying constant location info for " + location["name"])
            for key in const_location_info[location["name"]].keys():
                location[key] = const_location_info[location["name"]][key]

    return data


def inject_visiting_chefs(data: dict) -> dict:
    visiting_chefs_raw = open("data/visiting_chefs.json", "r").read()
    visiting_chefs = json.loads(visiting_chefs_raw)

    for location in data["locations"]:
        if location["name"] in visiting_chefs.keys():
            print("applying visiting chef info for " + location["name"])

            if "menus" in location.keys():
                menus = location["menus"]
            else:
                menus = []

            for chef in visiting_chefs[location["name"]]:
                chef_json = {
                    "id": 0,
                    "name": chef["chef"],
                    "description": chef["description"],
                    "price": 0,
                    "category": "Visiting Chef",
                    "eventId": 0
                }
                menus.append(chef_json)

            location["menus"] = menus

    return data
