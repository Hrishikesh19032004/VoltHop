from .common import stub
from .chargers import process_chargers
from .reviews import process_reviews
import modal

"""
Modal function which acts as orchestrator
"""


@stub.function(schedule=modal.Period(days=7), timeout=2700)
def plugshare_sentiment():
    print("==== Starting to Process Chargers =====")
    process_chargers.remote()

    print("==== Starting to Process Reviews =====")
    process_reviews.remote()

    return None


@stub.local_entrypoint()
def main():
    plugshare_sentiment.remote()
    print("Script Complete")
    return
