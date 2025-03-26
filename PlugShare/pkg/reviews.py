from .common import stub
import modal
import os
import requests
import pandas as pd
from datetime import datetime
import json
import time
from openai import OpenAI

"""
Script for sampling chargers, getting reviews for those chargers, processing them for sentiment analysis and finally saving the data in Tinybird
"""

MAX_NUM_REVIEWS = 1000
MAX_CHARGER_SAMPLE_SIZE = 150
PS_SLEEP = 1
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
        modal.Secret.from_name("OPENAI_KEY"),
    ],
    timeout=2700,
)
def process_reviews():
    start_time = time.time()
    TINYBIRD_KEY = os.environ["TINYBIRD_KEY"]
    OPENAI_KEY = os.environ["OPENAI_KEY"]

    # Define Functions
    def get_tb_data(url):
        cities_response = requests.get(url, params={"token": TINYBIRD_KEY})
        return pd.DataFrame(cities_response.json().get("data"))

    def process_reviews(charger_data):
        reviews = []
        for review in charger_data.get("reviews", []):
            processed_review = {
                "review_id": review.get("id"),
                "charger_id": charger_data.get("id"),
                "lang": review.get("language")
                if review.get("language") is not None
                else "eng",
                "created_at": review.get("created_at"),
                "peak_kw": review.get("kilowatts")
                if review.get("kilowatts") is not None
                else 0,
                "comment": review.get("comment", "").strip()[:300]
                if review.get("comment")
                else None,
                "had_problem": review.get("problem", 0),
                "problem_description": review.get("problem_description", "")[:300],
            }

            if review.get("spam_category") is not None:
                processed_review["comment"] = None
                processed_review["problem_description"] = ""

            reviews.append(processed_review)
        return reviews

    def check_dict_structure(input_dict):
        expected_keys = ["charging", "busy", "location"]
        allowed_types = (float, int)  # Accept both float and int

        for key in expected_keys:
            if key not in input_dict or not isinstance(input_dict[key], allowed_types):
                return {"charging": None, "busy": None, "location": None}

            # Cast integer values to float
            if isinstance(input_dict[key], int):
                input_dict[key] = float(input_dict[key])

            if not (0 <= input_dict[key] <= 1):
                return {"charging": None, "busy": None, "location": None}
        return input_dict

    def get_openai(review, client):
        prompt = (
            f"""
                Rate the following variables of an EV charger based on a user comment using a 0-1 scale. Default to 0.75 (good) if information is insufficient. Provide a JSON response with three variables and corresponding float values.

                1. charging: Assess speed and reliability of charging hardware and software.
                    - 1: Fast, flawless.
                    - 0.75: Decent speed, no major issues, or unknown.
                    - 0.5: Minor issues.
                    - 0.25: Slow, problematic.
                    - 0: Inoperative.

                2. busy: Evaluate crowding.
                    - 1: Not busy.
                    - 0.75: Slightly busy, no delay, or unknown.
                    - 0.5: Busy with no wait.
                    - 0.25: Busy with wait.
                    - 0: Overcrowded, long wait.

                3. location: Judge area quality and amenities.
                    - 1: Excellent area, ample amenities.
                    - 0.75: Good area, some amenities, or unknown.
                    - 0.5: Average.
                    - 0.25: Below average.
                    - 0: Poor, no amenities.

                Rate the following user-reported EV charger details:
                - Comment: {review.get("comment")}
                - Had Charging Problem(optional default 0): {review.get("had_problem")}
                - Problem Description: {review.get("problem_description")}
        """.strip()
            .replace("\t", "")
            .replace("  ", "")
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response = check_dict_structure(
            json.loads(
                response.model_dump().get("choices")[0].get("message").get("content")
            )
        )
        return {**review, **response}

    def get_charger_data(charger_id):
        time.sleep(PS_SLEEP)
        url = "https://api.plugshare.com/v3/locations/" + str(charger_id)
        response = requests.get(url, headers=HEADERS)
        return process_reviews(response.json())

    def process_review_data(reviews):
        client = OpenAI(api_key=OPENAI_KEY)
        gpt_reviews = [get_openai(review, client) for review in reviews]
        return [element for element in gpt_reviews if element is not None]

    def insert_reviews(reviews, table_name):
        for ev in reviews:
            ev["inserted_at"] = datetime.utcnow().isoformat()
        data = "\n".join([json.dumps(ev) for ev in reviews])

        params = {
            "name": table_name,
            "token": TINYBIRD_KEY,
        }

        r = requests.post(
            "https://api.us-east.tinybird.co/v0/events", params=params, data=data
        )

        print("TINYBIRD", r.text)
        return

    ### Run Logic
    def main():
        chargers_df = get_tb_data(
            "https://api.us-east.tinybird.co/v0/pipes/plugshare_distinct_chargers.json"
        )
        reviews_df = get_tb_data(
            "https://api.us-east.tinybird.co/v0/pipes/plugshare_distinct_reviews.json"
        )

        sample_size = min(len(chargers_df), MAX_CHARGER_SAMPLE_SIZE)
        chargers_df = chargers_df.sample(n=sample_size)

        print("Num Chargers", len(chargers_df))

        reviews_processed = 0
        for index, row in chargers_df.iterrows():
            processed_review_data = get_charger_data(row["charger_id"])
            reviews_df = get_tb_data(
                "https://api.us-east.tinybird.co/v0/pipes/plugshare_distinct_reviews.json"
            )
            if "review_id" in reviews_df.columns:
                ids_to_remove = set(reviews_df["review_id"])
            else:
                ids_to_remove = set()
            filtered_data = [
                d
                for d in processed_review_data
                if d.get("comment")
                and not d["comment"].isspace()
                and d["review_id"] not in ids_to_remove
            ]

            data_to_save = process_review_data(filtered_data)
            insert_reviews(data_to_save, "plugshare_reviews")
            reviews_processed += len(filtered_data)

            if reviews_processed >= MAX_NUM_REVIEWS:
                print(
                    "Limit reached, stopping... Num Processed: ",
                    reviews_processed,
                )
                break

        end_time = time.time()
        print("Run Time: ", end_time - start_time)

    return main()
