import json
import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NerdGraphClientError(Exception):
    """Custom error for NerdGraphClient."""
    pass


class NerdGraphClient:
    def __init__(self, api_key=None, url=None):
        self.api_key = api_key or os.getenv("NEW_RELIC_USER_KEY")
        self.url = url or "https://api.newrelic.com/graphql"

    def _build_headers(self):
        return {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }

    def send_query(self, query, variables=None):
        payload = {"query": query}
        if variables is not None:  # Add variables to the payload only if provided
            payload["variables"] = variables

        headers = self._build_headers()

        try:
            logging.debug(f"Sending request to the GraphQL endpoint {self.url} with payload: {json.dumps(payload)}")
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Request error occurred: {str(e)}")
            raise NerdGraphClientError(str(e))
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            raise NerdGraphClientError("An unexpected error occurred")
        else:
            logging.debug(f"Response: {response.json()}")
            return response.json()
