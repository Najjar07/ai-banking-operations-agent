import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "logs",
    "prediction_logs.json"
)


def save_log(log_data):

    log_data["timestamp"] = str(datetime.now())

    logs = [log_data]

    os.makedirs("logs", exist_ok=True)

    # WRITE FILE
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)
