import new_relic.ApmEntityCollector as ApmEntityCollector
import new_relic.AlertCoverageCollector as AlertCoverageCollector
import new_relic.NerdGraphClient as NerdGraphClient
import CsvFileManager as CsvFileManager
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="w"
)


def main():
    """
    This is the main function.
    :return: None
    """

    logging.info("Starting the application.")

    # Create required objects.
    nerdgraph = NerdGraphClient.NerdGraphClient()  # Create a NerdGraphClient object
    apm_collector = ApmEntityCollector.ApmEntityCollector()  # Create an ApmEntityCollector object
    alert_collector = AlertCoverageCollector.AlertCoverageCollector()  # Create an AlertCoverageCollector object
    csv_manager = CsvFileManager.CsvFileManager("output.csv")  # Create a CsvFileManager object

    # Get a list of entities for a given account
    apm_entities = apm_collector.get_entities(nerdgraph)

    # Get alert coverage data for a given account
    entity_data = alert_collector.get_alert_reporting_data(apm_entities, nerdgraph)

    # Write the data to a CSV file
    csv_manager.write_dicts_to_csv(entity_data)

    logging.info("Finished the application.")


if __name__ == '__main__':
    main()
