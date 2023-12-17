import sys
import datetime
import os
import re
import argparse

from datetime import datetime, timedelta

from dotenv import load_dotenv
from services.clockify_api import ClockifyApi
from services.tempo_api import TempoApiV3


def load_configuration():
    required_keys = ["API_KEY", "WORKSPACE_ID", "USER_ID", "CLIENT_ID_TO_SYNC", "TEMPO_TOKEN",
                     "TEMPO_WORKER_ID", "TEMPO_TAG_ID_SYNCHRONIZED"]

    config = {}
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Key '{key}' missing or invalid.")
        config[key] = value

    return config


## Todo: Move to entry model
def convert_to_seconds(work_time_string: str) -> int:
    if not work_time_string:
        return 0

    match = re.search(r'(\d{1,2})H', work_time_string)
    hours = match.group(1) if match else 0
    match = re.search(r'(\d{1,2})M', work_time_string)
    minutes = match.group(1) if match else 0
    match = re.search(r'(\d{1,2})S', work_time_string)
    seconds = match.group(1) if match else 0

    return (int(hours) * 3600) + (int(minutes) * 60) + int(seconds)


# Todo: check if tag synchronized exists, if not create, remove from config
def main(config, days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    clockify = ClockifyApi(config)
    tempo = TempoApiV3(config)

    print(f"Synchronizing time entries for clientId: {config['CLIENT_ID_TO_SYNC']}")

    time_entries = clockify.get_time_entries(start_date, end_date)

    for entry in time_entries:
        if entry["tagIds"] and config["TEMPO_TAG_ID_SYNCHRONIZED"] in entry["tagIds"]:
            print(f"Already synced entry: {entry['timeInterval']['start']}, skipping")
            continue  # Already synchronized => skip
        if not entry["projectId"] or not entry["taskId"]:
            continue  # No project or task assigned => skip

        project = clockify.get_project_by_id(entry["projectId"])
        task = clockify.get_task_by_id(entry["taskId"], entry["projectId"])

        if task and project:
            time_spent_seconds = convert_to_seconds(entry["timeInterval"]["duration"])
            if project["client_id"] == config["CLIENT_ID_TO_SYNC"] and time_spent_seconds > 59:
                issue_key = task["name"]
                description = entry["description"]
                start_date = entry["timeInterval"]["start"].split('T')[0]
                start_time = datetime.strptime(entry["timeInterval"]["start"], '%Y-%m-%dT%H:%M:%SZ').strftime(
                    '%H:%M:%S')

                account_key = project["name"]
                response_code = tempo.create_tempo_entry(issue_key, time_spent_seconds, start_date, start_time,
                                                         description, account_key)
                if response_code == 200:
                    if entry["tagIds"] is None:
                        entry["tagIds"] = []
                    entry["tagIds"].append(config["TEMPO_TAG_ID_SYNCHRONIZED"])
                    clockify.update_time_entry(entry["id"], entry)
                    print(f"Added Tempo worklog for issueKey: {issue_key}")
                else:
                    print(f"ERROR: Response from tempo API: {response_code}. Failed to create entry: {entry['timeInterval']['start']}, skipping")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Usage: run.py -d {days}')
    parser.add_argument('-d', '--days', type=int, required=True, help='Days in the past to sync time entries from.')
    args = parser.parse_args()

    # Load .env file
    load_dotenv()

    try:
        main(load_configuration(), args.days)
    except ValueError as e:
        print("Exception:", e)
