import requests


# https://apidocs.tempo.io/v3/#worklogs
class TempoApiV3:
    def __init__(self, config):
        self.config = config

    def create_tempo_entry(self, issue_key: str, time_spent_seconds: int, start_date: str, start_time: str, description: str, account_key: str):
        url = "https://api.tempo.io/core/3/worklogs"
        headers = {
            "Authorization": f"Bearer {self.config['TEMPO_TOKEN']}",
            "Content-Type": "application/json"
        }
        data = {
            "attributes": [{
                "key": "_Account_",
                "value": f"{account_key}"
            }],
            "billableSeconds": time_spent_seconds,
            "description": description,
            "startDate": start_date,
            "startTime": start_time,
            "timeSpentSeconds": time_spent_seconds,
            "issueKey": issue_key,
            "authorAccountId": self.config["TEMPO_WORKER_ID"]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code
