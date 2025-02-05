import requests
from requests.auth import HTTPBasicAuth


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


class TempoApiV4:
    def __init__(self, config):
        self.config = config

    def get_issue_id(self, issue_key: str):
        jira_url = f"{self.config['JIRA_BASE_URL']}/rest/api/2/issue/{issue_key}"
        headers = {"Accept": "application/json"}
        response = requests.get(jira_url, headers=headers, auth=HTTPBasicAuth(self.config['JIRA_EMAIL'], self.config['JIRA_TOKEN']))
        if response.status_code == 200:
            return response.json().get('id')
        else:
            raise Exception(f"Failed to fetch issue ID for {issue_key}: {response.status_code} - {response.text}")

    def create_tempo_entry(self, issue_key: str, time_spent_seconds: int, start_date: str, start_time: str, description: str, account_key: str):
        issue_id = self.get_issue_id(issue_key)
        url = "https://api.tempo.io/4/worklogs"
        headers = {
            "Authorization": f"Bearer {self.config['TEMPO_TOKEN']}",
            "Content-Type": "application/json"
        }
        data = {
            "issueId": issue_id,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": start_date,
            "startTime": start_time,
            "description": description,
            "authorAccountId": self.config["TEMPO_WORKER_ID"],
            "attributes": [
                {
                    "key": "_Account_",
                    "value": account_key
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code