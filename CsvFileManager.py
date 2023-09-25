import csv
import os


class CsvFileManager:

    def __init__(self, file_name):
        self.file_name = file_name
        # self.class_directory = os.path.dirname(os.path.realpath(__file__))
        # self.parent_directory = os.path.dirname(self.class_directory)
        # self.csv_directory = 'csv_files'
        # self.csv_files_directory = os.path.join(self.parent_directory, self.csv_directory, self.file_name)

    def write_csv(self, data):

        try:
            # fieldnames = list(data[0].keys())
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in data:
                    print(row)
                    #writer.writerow(row)
                file.close()
        except FileNotFoundError:
            print(f"File not found: {self.file_name}. Exiting the application.")
            exit()
        except PermissionError:
            print(f"Permission denied: {self.file_name}. Exiting the application.")
            exit()
        except IOError as e:
            print(f"IOError: {e}. Exiting the application.")
            exit()
        except Exception as e:
            print(f"Exception: {e}. Exiting the application.")
            exit()

    def write_dicts_to_csv(self, list_of_dicts):

        headers = ['name', 'guid', 'alert_severity', 'reporting']
        # Ensure there's at least one dictionary in the list
        if not list_of_dicts:
            print("Error: The list is empty. Nothing to write.")
            return

        # Ensure all dictionaries have the same set of keys
        if any(set(d.keys()) != set(headers) for d in list_of_dicts):
            print("Error: All dictionaries must have the same set of keys.")
            return

        with open(self.file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # Write the header row
            writer.writeheader()

            # Write the rows
            writer.writerows(list_of_dicts)

            file.close()
