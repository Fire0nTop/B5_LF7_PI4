import time
from time import sleep

from SharedData import data_lock, dataBaseChanges

class DatabaseChangeDetector:
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
            self.current_data = self.db.findAll()
            self.compare_data()
            self.previous_data = self.current_data  # Update previous data
            sleep(self.check_interval)  # Wait before the next check

    def compare_data(self):
        """
        Compares previous and current data, logs changes.
        """
        # Check if status matches
        if self.previous_data['status'] != self.current_data['status']:
            print(f"Status changed from {self.previous_data['status']} to {self.current_data['status']}")

        # Initialize dictionaries for easy comparison by key_id
        previous_records = {record['key_id']: record for record in self.previous_data['records']}
        current_records = {record['key_id']: record for record in self.current_data['records']}

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
                #print("Modified record:")
                #print(f"Previous: {previous_records[key]}")
                #print(f"Current: {current_records[key]}")
                with data_lock:
                    dataBaseChanges.append({
                        'previous': previous_records[key],
                        'current': current_records[key]
                    })