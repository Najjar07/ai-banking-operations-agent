import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

LOGS_DIR = os.path.join(BASE_DIR, "logs")

LOG_FILE = os.path.join(
    LOGS_DIR,
    "prediction_logs.json"
)


def save_log(log_data):

    # Create logs folder if missing
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Read existing logs
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)

    except:
        logs = []

    # Add timestamp
    log_data["timestamp"] = str(datetime.now())

    # Append log
    logs.append(log_data)

    # Save logs
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)