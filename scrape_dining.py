# "scrape_dining.py" from TigerDine-Supplemental-API
# Copyright (c) 2026 NinjaCheetah/Campbell Bagley
# https://github.com/NinjaCheetah/TigerDine-Supplemental-API
#
# Functions to scrape the RIT dining website and save the data for later injection.

import json
import re

from bs4 import BeautifulSoup
import requests


# Scrapes the visiting chefs list from the dining site and saves it in a TigerCenter API compatible format.
def parse_visiting_chefs(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    heading = next(
        (
            h2 for h2 in soup.find_all("h2")
            if "Today's Visiting Chefs" in h2.get_text(" ", strip=True)
        ),
        None
    )

    if heading is None:
        print("visiting chefs header not found")
        return results

    section = heading.find_parent("div", class_="col-12")

    if section is None:
        print("visiting chefs section not found")
        return results

    for location_div in section.find_all("div", recursive=False):
        location_name_tag = location_div.select_one(
            "a > p.h5"
        )

        if location_name_tag is None:
            continue

        location_name = location_name_tag.get_text(strip=True)

        for chef_item in location_div.select("ul > li"):
            chef_link = chef_item.find("a")

            if chef_link is None:
                continue

            chef_text = chef_link.get_text(" ", strip=True)

            match = re.match(
                r"^(.*?):\s*(.*?)\s*-\s*(.*?)$",
                chef_text
            )

            if match is None:
                continue

            chef_name = match.group(1).strip()
            start_time = match.group(2).strip()
            end_time = match.group(3).strip()

            chef_id = chef_link.get("chefid")
            popup = (
                chef_item.find("div", id=f"{chef_id}-chef-holder")
                if chef_id
                else chef_item.select_one("div.pop-up")
            )

            description_tag = (
                popup.find("em") if popup else None
            )

            description = (
                description_tag.get_text(strip=True)
                if description_tag
                else None
            )

            # Format the name + times into the joined string format that the TigerCenter API uses so that we can
            # inject it.
            tc_chef_string = chef_name + " ("

            start_time_pieces = start_time.split(":")
            start_am_pm_pieces = start_time_pieces[1].split(" ")
            tc_chef_string += start_time_pieces[0] + " " + start_am_pm_pieces[1] + "-"

            end_time_pieces = end_time.split(":")
            end_am_pm_pieces = end_time_pieces[1].split(" ")
            tc_chef_string += end_time_pieces[0] + " " + end_am_pm_pieces[1]

            tc_chef_string += ")"

            if location_name in results.keys():
                location = results[location_name]
            else:
                location = []

            location.append({
                #"location": location_name,
                "chef": tc_chef_string,
                "description": description,
            })
            results[location_name] = location

    return results


def main():
    print("starting scrape script")
    try:
        response = requests.get(
            url="https://www.rit.edu/dining/",
            stream=False,
            timeout=5
        )
        visiting_chefs = parse_visiting_chefs(response.text)
        print("got visiting chefs! output:")
        print(visiting_chefs)

        print("saving data...")
        visiting_chefs_json = json.dumps(visiting_chefs, indent=4)
        open("data/visiting_chefs.json", "w").write(visiting_chefs_json)

    except requests.exceptions.ConnectionError:
        return None


if __name__ == "__main__":
    main()
