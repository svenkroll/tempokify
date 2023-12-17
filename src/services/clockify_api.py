import requests

from models.task import Task, TaskSchema
from models.project import Project, ProjectSchema


class ClockifyApi:
    BASE_URL = "https://api.clockify.me/api/v1"

    def __init__(self, config):
        self.config = config
        self.workspace_id = config['WORKSPACE_ID']
        self.api_key = config['API_KEY']
        self.user_id = self.config['USER_ID']

    def update_time_entry(self, time_entry_id: str, entry) -> int:
        url = f"{self.BASE_URL}/workspaces/{self.workspace_id}/time-entries/{time_entry_id}"

        data = {
            "billable": entry["billable"],
            "customFields": [],
            "description": entry["description"],
            "end": entry["timeInterval"]["end"],
            "id": entry["id"],
            "projectId": entry["projectId"],
            "start": entry["timeInterval"]["start"],
            "tagIds": entry["tagIds"],
            "taskId": entry["taskId"],
        }

        headers = {"X-Api-Key": self.api_key}
        response = requests.put(url, headers=headers, json=data)
        return response.status_code

    def get_time_entries(self, start_date, end_date):
        url = f"{self.BASE_URL}/workspaces/{self.workspace_id}/user/{self.user_id}/time-entries"

        start_format = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_format = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        # TODO: Iterate through pages
        params = {
            "start": start_format,
            "end": end_format,
            "page-size": 500
        }
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def get_project_by_id(self, project_id: str):
        url = f"{self.BASE_URL}/workspaces/{self.workspace_id}/projects/{project_id}"
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            project_schema = ProjectSchema()
            project = project_schema.load(response.json())
            return project
        else:
            raise Exception(f"Fehler beim Abrufen des Projekts: {response.status_code}")

    def get_task_by_id(self, task_id: str, project_id: str) -> Task:
        url = f"{self.BASE_URL}/workspaces/{self.workspace_id}/projects/{project_id}/tasks/{task_id}"
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            task_schema = TaskSchema()
            task = task_schema.load(response.json())
            return task
        else:
            raise Exception(f"Could not fetch task from Clockify: {response.status_code}")
