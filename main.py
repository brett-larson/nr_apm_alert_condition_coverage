import new_relic.ApmEntityCollector as ApmEntityCollector
import new_relic.NerdGraphClient as NerdGraphClient
import logging

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="w"
)


def main():
    nerdgraph = NerdGraphClient.NerdGraphClient()
    collector = ApmEntityCollector.ApmEntityCollector()
    entities = collector.get_entities(nerdgraph)
    print(entities)


if __name__ == '__main__':
    main()
