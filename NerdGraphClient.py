"""
    The NerdGraphClient is used to execute GraphQL queries against the New Relic API.
"""
import json
import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class NerdGraphClient:
    """
    This class is used to execute GraphQL queries against the New Relic API.
    """

    def __init__(self):
        """
        This is the constructor for the NerdGraphClient class.
        """
        self.api_key = os.getenv("NEW_RELIC_USER_KEY")
        self.url = "https://api.newrelic.com/graphql"

    def _build_headers(self):
        """
        This private function builds the headers for the API request.
        :return: A dictionary containing the headers.
        """

        return {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }

    def send_query(self, query, variables=None):
        """
        This private function executes a GraphQL query against the New Relic API. Variables can be passed to the query.
        If no variables are passed, the query will be executed without variables. Executing this function without
        variables will fail if the query requires variables. For this class, variables are required.
        :param query: The NerdGraph query to execute.
        :param variables: The variables to pass to the query.
        :return: The JSON response from the API.
        """

        payload = {"query": query}  # The GraphQL query

        if variables:
            payload["variables"] = variables
        else:
            logging.error("Variables must be passed to the query.")
            exit(1)

        headers = self._build_headers()  # Build the headers for the API request

        try:
            logging.info(f"Sending request with {variables} to the GraphQL endpoint {self.url}")
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            logging.info(f"Response: {response.json()}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(e)
            exit(1)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            exit(1)

        return response.json()
