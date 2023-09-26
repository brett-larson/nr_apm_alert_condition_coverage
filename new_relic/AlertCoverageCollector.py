import logging


class AlertCoverageCollector:
    """
    This class contains functions to get the alert coverage for APM entities in a given account.
    """

    def __init__(self):
        self.entities = []  # List of dictionaries containing APM entities

    def _build_query(self, entity_guid):
        """
        This function returns the query to get the average transaction time for a given APM entity.
        :param entity_guid: The entity GUID.
        :return: The GraphQL query and variables.
        """

        query_variables = {
            "entity_guid": entity_guid
        }

        graphql_query = """
        query ($entity_guid: EntityGuid!) {
          actor {
            entity(guid: $entity_guid) {
              alertSeverity
              reporting
            }
          }
        }
        """

        return graphql_query, query_variables

    def get_alert_reporting_data(self, entity_list, nerdgraph_client):
        """
        This function returns a list of entities for a given account.
        :return: A list of entities.
        """
        try:
            for entity in entity_list:
                query, variables = self._build_query(entity["guid"])
                response = nerdgraph_client.send_query(query, variables)

                alert = response["data"]["actor"]["entity"]["alertSeverity"]
                if alert == "NOT_CONFIGURED":
                    entity["alert_severity"] = "NOT CONFIGURED"
                elif alert == "CRITICAL":
                    entity["alert_severity"] = "CONFIGURED"
                elif alert == "WARNING":
                    entity["alert_severity"] = "CONFIGURED"
                elif alert == "NOT_ALERTING":
                    entity["alert_severity"] = "CONFIGURED"
                else:
                    entity["alert_severity"] = "UNKNOWN"

                entity["reporting"] = response["data"]["actor"]["entity"]["reporting"]

                self.entities.append(entity)
        except KeyError as e:
            logging.error(f'Error: {e}.')
            raise
        except Exception as e:
            logging.error(f'Error: {e}.')
            raise

        return self.entities
