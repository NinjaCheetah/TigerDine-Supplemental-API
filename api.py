# "api.py" from TigerDine-Supplemental-API
# Copyright (c) 2026 NinjaCheetah/Campbell Bagley
# https://github.com/NinjaCheetah/TigerDine-Supplemental-API
#
# Defines the main FastAPI app and defines the one API route that it offers.

from datetime import date as dt

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

from injections import inject_const_location_info, inject_visiting_chefs


app = FastAPI()


@app.get(
    "/api/dining/dining-all",
    response_class=JSONResponse,
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "Gets dining-all from TigerCenter with supplemental information injected."
        }
    }
)
async def dining_all(date: str = ""):
    try:
        response = requests.get(
            url="https://tigercenter.rit.edu/tigerCenterApi/tc/dining-all?date=" + date,
            stream=False,
            timeout=2
        )

        response_json = response.json()

        # Inject constant location info changes into the response.
        response_json = inject_const_location_info(response_json)

        # These injections should only happen if the requested date is today's date. Unfortunately we can only get
        # today's info from the RIT dining website so we're stuck with this limitation.
        if str(dt.today()) == date:
            print("request made for today, performing all injections")

            # Inject visiting chef info into the response.
            response_json = inject_visiting_chefs(response_json)

        return JSONResponse(response_json)

    except requests.exceptions.ConnectionError:
        return None
