import NerdGraphClient as nerdgraph
import logging


def main():

    client = nerdgraph.NerdGraphClient()
    try:
        response = client.send_query(query="YOUR_QUERY", variables={"key": "value"})
    except nerdgraph.NerdGraphClientError as e:
        logging.error(f"Failed to send query: {str(e)}")
    else:
        # Process the response
        pass
