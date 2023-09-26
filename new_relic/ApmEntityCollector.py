import logging
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()


class ApmEntityCollector:
    """
    This class contains the methods to get a list of entity names and GUId's for a given account. The get_entities
    method is the primary method called.
    """

    def __init__(self):
        self.account_id = os.getenv("NEW_RELIC_ACCOUNT_ID")
        self.entities = []  # List of dictionaries containing APM entity names and GUIDs

    def _build_queries(self, cursor=None):
        """
        This private function returns the query to get a list of APM entities for a given account. There are two
        queries, one with a cursor and one without. The cursor is used to get the next page of results.
        :return: The NerdGraph query and variables.
        """

        logging.debug("Building query.")

        if cursor:
            logging.debug("Cursor is not None. Building query with cursor.")

            # Query variables with a cursor
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'",
                "cursor": cursor
            }

            # Query with a cursor
            graphql_query = """
                query ($entity_search_query: String!, $cursor: String!) {
                  actor {
                    entitySearch(query: $entity_search_query, options: {limit: 10}) {
                      results(cursor: $cursor) {
                        nextCursor
                        entities {
                          guid
                          name
                        }
                      }
                    }
                  }
                }
                """
        else:
            logging.debug("Cursor is None. Building query without cursor.")

            # Query variables without a cursor
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'"
            }

            # Query without a cursor
            graphql_query = """
                query ($entity_search_query: String!) {
                  actor {
                    entitySearch(query: $entity_search_query, options: {limit: 2}) {
                      results {
                        nextCursor
                        entities {
                          guid
                          name
                        }
                      }
                    }
                  }
                }
                """

        return graphql_query, query_variables

    def get_entities(self, nerdgraph_client):
        """
        This method is the primary method called to get a list of entity names and GUIDs for a given account.
        :param nerdgraph_client: A NerdGraphClient object.
        :return: A list of dictionaries containing entity names and GUIDs.
        """

        # next_cursor = None  # Initialize the next cursor to None

        query, variables = self._build_queries()  # Get the query and variables

        # Send the query to the API and process the response.
        response = nerdgraph_client.send_query(query, variables)
        next_cursor = self._check_next_cursor(response)
        self._process_response(response)

        while next_cursor:
            # While there is a next cursor, send the query to the API and process the response.
            query, variables = self._build_queries(next_cursor)
            response = nerdgraph_client.send_query(query, variables)
            next_cursor = self._check_next_cursor(response)
            self._process_response(response)
            sleep(0.5)  # Sleep for 0.5 seconds to avoid rate limiting.

        return self.entities

    @staticmethod
    def _check_next_cursor(response):
        """
        This private function checks the response for the next cursor. If there is a next cursor, it is returned.
        If there is not a next cursor, None is returned.
        :param response:
        :return:
        """

        try:
            next_cursor = response["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
        except KeyError:
            logging.error("KeyError: 'nextCursor' not found in response.")
            next_cursor = None

        return next_cursor

    def _process_response(self, response):
        """
        This private function processes the response from the API request. This includes getting the next cursor,
        if any, and appending the entities to the entities list.
        :param response: The JSON response from the API request.
        :return: The next cursor, if any.
        """

        try:
            next_cursor = response["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
        except KeyError:
            logging.error("KeyError: 'nextCursor' not found in response.")
            next_cursor = None

        entities = response["data"]["actor"]["entitySearch"]["results"]["entities"]

        # Append the entities to the entities list
        try:
            for entity in entities:
                logging.info(f"Appending entity: {entity['name']}")
                self.entities.append(entity)
        except KeyError:
            logging.error("KeyError: 'name' not found in entity.")


