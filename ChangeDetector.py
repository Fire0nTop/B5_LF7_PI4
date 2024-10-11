import time
from time import sleep


def compare_data(previous_data, current_data):
    """
    Compares previous and current data, logs changes.

    Args:
        previous_data: The data from the last check.
        current_data: The data from the current check.
    """
    # Check if status matches
    if previous_data['status'] != current_data['status']:
        print(f"Status changed from {previous_data['status']} to {current_data['status']}")

    # Initialize dictionaries for easy comparison by key_id
    previous_records = {record['key_id']: record for record in previous_data['records']}
    current_records = {record['key_id']: record for record in current_data['records']}

    # Find added and removed records
    added_keys = set(current_records) - set(previous_records)
    removed_keys = set(previous_records) - set(current_records)

    # Log added records
    if added_keys:
        print("Added records:")
        for key in added_keys:
            print(current_records[key])

    # Log removed records
    if removed_keys:
        print("Removed records:")
        for key in removed_keys:
            print(previous_records[key])

    # Check for modified records
    for key in current_records:
        if key in previous_records and previous_records[key] != current_records[key]:
            print("Modified record:")
            print(f"Previous: {previous_records[key]}")
            print(f"Current: {current_records[key]}")


class ChangeDetector:
    def __init__(self, database, check_interval=5):
        """
        Initializes the ChangeDetector instance.

        Args:
            database: An instance of the DataBase class.
            check_interval: Time interval (in seconds) to check for changes.
        """
        self.db = database
        self.check_interval = check_interval
        self.previous_data = self.db.findAll()  # Initialize previous data

    def detect_changes(self):
        """
        Continuously checks for changes in the database at specified intervals.
        """
        while True:
            current_data = self.db.findAll()
            compare_data(self.previous_data, current_data)
            sleep(self.check_interval)  # Wait before the next check
            self.previous_data = current_data  # Update previous data

