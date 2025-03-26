import modal
import os
import requests
import pandas as pd
from datetime import datetime
import json
import time
import random
from .common import stub

"""
Script which collects chargers by looking at sample top 1000 US cities lat long (randomly jittered), and recording their data in Tinybird
"""


NUM_CHARGERS = 5000
CITIES_SAMPLE = 25
PS_SLEEP = 1.5
API_COUNT = 500
NETWORK_NAMES = {8: "Tesla", 19: "EVgo", 47: "Electrify_America", 1: "ChargePoint"}
TB_URL_CITIES = "https://api.us-east.tinybird.co/v0/pipes/plugshare_cities_select.json"
TB_URL_CHARGERS = (
    "https://api.us-east.tinybird.co/v0/pipes/plugshare_distinct_chargers.json"
)

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Authorization": "Basic d2ViX3YyOkVOanNuUE54NHhXeHVkODU=",
    "Dnt": "1",
    "Origin": "https://www.plugshare.com",
    "Referer": "https://www.plugshare.com/",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


@stub.function(
    secrets=[
        modal.Secret.from_name("TINYBIRD_KEY"),
    ],
    timeout=600
)
def process_chargers():
    # Define Variables
    TINYBIRD_KEY = os.environ["TINYBIRD_KEY"]

    # Define functions
    def get_tb_data(url):
        cities_response = requests.get(url, params={"token": TINYBIRD_KEY})
        return pd.DataFrame(cities_response.json().get("data"))

    def get_ps_chargers(city):
        try:
            time.sleep(PS_SLEEP)
            print("City ", city["latitude"], ",", city["longitude"])
            url = "https://api.plugshare.com/v3/locations/region"
            params = {
                "access": 1,
                "count": API_COUNT,
                "exclude_poi_names": "dealership",
                "latitude": city["latitude"] + (random.random() * 4 - 2),
                "longitude": city["longitude"] + (random.random() * 4 - 2),
                "minimal": 0,
                "minimum_power": 149,
                "networks": "1,47,19,8",
                "outlets": '[{"connector":6,"power":1},{"connector":13,"power":0},{"connector":6,"power":0}]',
                "spanLat": 5,
                "spanLng": 5,
            }

            # Headers for the GET request

            response = requests.get(url, params=params, headers=HEADERS)
            return response.json()
        except Exception as e:
            print(f"Error occurred: {e}")
        return None

    def process_charger(charger):
        network_id = 999
        if charger.get("stations") and len(charger["stations"]) > 0:
            network_id = charger["stations"][0].get("network_id")

        # Construct kilowatts list, filtering out None values
        kilowatts = [
            outlet.get("kilowatts")
            for station in charger.get("stations", [])
            for outlet in station.get("outlets", [])
            if outlet.get("kilowatts") is not None
        ]

        # Return the processed data with defaulting to 0 for min_kw and max_kw if no valid kilowatt values
        return {
            "charger_id": charger["id"],
            "address": charger.get("address", "No address provided"),
            "network_id": network_id,
            "network_name": NETWORK_NAMES.get(network_id, "Unknown"),
            "min_kw": min(kilowatts) if kilowatts else 0,
            "max_kw": max(kilowatts) if kilowatts else 0,
            "count_stations": len(charger.get("stations", [])),
            "lat": charger.get("latitude"),
            "long": charger.get("longitude"),
        }

    def insert_chargers(chargers, table_name, chargers_df):
        processed_chargers_df = pd.DataFrame(
            [process_charger(charger) for charger in chargers]
        )

        if not chargers_df.empty:
            processed_chargers_df = processed_chargers_df[
                ~processed_chargers_df["charger_id"].isin(chargers_df["charger_id"])
            ]

        # Early exit if there are no chargers to add
        if processed_chargers_df.empty:
            print("No chargers to add")
            return
        print("Num chargers to add", len(processed_chargers_df))

        processed_chargers_df["inserted_at"] = datetime.utcnow().isoformat()

        data = "\n".join(
            json.dumps(event) for event in processed_chargers_df.to_dict("records")
        )

        params = {"name": table_name, "token": TINYBIRD_KEY}
        response = requests.post(
            "https://api.us-east.tinybird.co/v0/events", params=params, data=data
        )

        print(response.text)

    ### Run Logic
    def main():
        cities_df = get_tb_data(TB_URL_CITIES).sample(CITIES_SAMPLE)

        for index, row in cities_df.iterrows():
            chargers_df = get_tb_data(TB_URL_CHARGERS)
            if chargers_df.size > NUM_CHARGERS:
                return f"At charger sample limit, num chargers: {chargers_df.size}"

            results = get_ps_chargers(row)
            if results is not None:
                insert_chargers(results, "plugshare_chargers", chargers_df)
        return

    return main()
