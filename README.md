# New Relic APM Alert Coverage Report
## Description
This Python program provides information about New Relic APM entities within a given account. Specifically, this program creates a CSV file with APM Entity Name and GUID, the current reporting status (i.e., if the entity is actively sending data to New Relic), and whether or not the entity is covered by Alert Conditions.


## Requirements
A New Relic User API Key is required to run these queries. User API Key permissions are inherited from the New Relic user permissions from the user who created the key. Please review the [New Relic Docs](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/#user-key) for more information.

The following packages are required to run this code and are included in the `requirements.txt` file:
- dotenv
- requests

This program was written with Python [v3.11.4](https://www.python.org/downloads/release/python-3114/).

## .env
This project is set up to leverage a `.env` file for storing your New Relic User API Key and account number, which are represented by the following variables:
- NEW_RELIC_USER_KEY
- NEW_RELIC_ACCOUNT_ID

## How to Run
This program can be run from your favorite Python IDE. However, it can be adapted to run within your desired infrastructure.

1. Create a copy of the source code on your local machine.
2. Create a `.env` file with the abovementioned two variables.
3. Install all required Python packages.
4. Run the Python program.

The completion time will vary based on the number of APM entities within the specified account.
