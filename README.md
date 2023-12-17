# [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R8QT94J)  Synchronize Clockify worklogs to Tempo (using Jira with Tempo plugin)

This project provides a Python script to synchronize worklogs from Clockify to Tempo.

One of my clients, like many others, uses Tempo within their Jira Cloud for time tracking. 
I opted for Clockify some time ago because of its ease of use and convenience, despite the very complex configuration and reporting options.

In order not to have to use the cumbersome Tempo Tracking, tempokify was created which synchronizes the Clockify entries into the Tempo cloud.

The script supports assigning Clockify time entries to Jira tickets and Tempo accounts.

## Prerequisites

### Clockify time entries
To be able to sync the time entries as worklogs to Tempo, the clockify entries needs to follow some rules

1. Time entries only get synced when they are related to a project

   To be able to assign Tempo worklogs to accounts, the Clockify project name must be the key of the Tempo account. 
   Currently i don't use the PRO version providing custom fields, this would enable us to store the account key in a separated field so we can set the project name to something readable. Possible i do that later.

   You can get a list of the accounts and their keys curl'ing https://api.tempo.io/core/3/accounts


2. Time entries only get synced when they are related to a task

   Tempo worklogs are assigned to Jira tickets, a good option for this is to create a task for each Jira ticket you're working on.

### macOS Setup

Before setting up the virtual environment, ensure you have Python installed on your macOS. If you haven't, you can install it using [Homebrew](https://brew.sh/):

\```bash
brew install python3
\```

This will install Python 3 and the `pip` package manager.

## Setting Up the Virtual Environment

To isolate the project dependencies, we'll use a virtual environment. Here's how to set it up:

1. Navigate to the project directory.
2. Create a virtual environment named `.venv`:

\```bash
python3 -m venv .venv
\```

3. Activate the virtual environment:

\```bash
source .venv/bin/activate
\```

You'll know it's activated once your terminal prompt changes to show the `.venv` name.

## Installing Dependencies

Once inside the virtual environment, install the required packages with:

\```bash
pip install -r requirements.txt
\```

## Configuration

Before running the script, you'll need to set up your configuration:

1. Copy the `.env.dist` file:

\```bash
cp .env.dist .env
\```

2. Edit the `.env` file with your Jira details:

- `API_KEY=`: See https://docs.clockify.me/#section/Authentication
- `WORKSPACE_ID=`: The Clockify workspace we source entries from (https://docs.clockify.me/#tag/Workspace)
- `USER_ID=`: Your Clockify user id, we only sync your time entries.
- `CLIENT_ID_TO_SYNC=`: We only synchronize Clockify entries for a single Clockify client (https://app.clockify.me/clients)
- `TEMPO_TOKEN=`: See https://apidocs.tempo.io/v3/ for auth, create a user token and add it here
- `TEMPO_TAG_ID_SYNCHRONIZED=`: The id of the tag in clockify, that is set when we synchronized the entry to tempo. This tag ensure's we do not duplicate worklogs.
- `TEMPO_WORKER_ID=`: The id of your account inside Tempo to relate the worklogs to you. I used the network console of my browser while adding worklogs manually in Tempo to get the id. 

## Running the Script

To execute the program:

The script requires as parameter "days" a number to determines the past period from today in days for which the clockify timesheets are to be synchronized.

\```bash
python run.py -d {days}
\```
