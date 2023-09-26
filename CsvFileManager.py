import csv
import logging
import os


class CsvFileManager:
    """
    This class contains functions for writing data to a CSV file.
    """

    def __init__(self, file_name):
        self.file_name = file_name

        '''
        Uncomment this code if you want to write the CSV file to a different directory.
        self.class_directory = os.path.dirname(os.path.realpath(__file__))
        self.parent_directory = os.path.dirname(self.class_directory)
        self.csv_directory = 'csv_files'
        self.csv_files_directory = os.path.join(self.parent_directory, self.csv_directory, self.file_name)
        '''

    def write_dicts_to_csv(self, list_of_dicts):
        """
        This function writes a list of dictionaries to a CSV file.
        :param list_of_dicts: A list of dictionaries.
        :return: None
        """

        headers = ['name', 'guid', 'alert_severity', 'reporting']
        # Ensure there's at least one dictionary in the list
        if not list_of_dicts:
            print("Error: The list is empty. Nothing to write.")
            return

        # Ensure all dictionaries have the same set of keys
        if any(set(d.keys()) != set(headers) for d in list_of_dicts):
            logging.error("Error: All dictionaries must have the same set of keys.")
            return
        try:
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)

                # Write the header row
                writer.writeheader()

                # Write the rows
                writer.writerows(list_of_dicts)

        except IOError as e:
            logging.error(f'Error: {e}.')
            raise
        except Exception as e:
            logging.error(f'Error: {e}.')
            raise
