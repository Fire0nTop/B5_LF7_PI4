from time import sleep


class ChangeDetector:
    def __init__(self, check_interval=1):
        """
        Initializes the ChangeDetector instance.

        Args:
            check_interval: Time interval (in seconds) to check for changes.
        """
        self.check_interval = check_interval
        self.previous_data = None
        self.current_data = None

    def detect_changes(self):
        """
        Continuously checks for changes at specified intervals.
        """
        while True:
            self.current_data = self.fetch_data()
            if self.previous_data is not None:
                self.compare_data()
            self.previous_data = self.current_data  # Update previous data
            sleep(self.check_interval)  # Wait before the next check

    def fetch_data(self):
        """
        Fetches current data. This method should be implemented by subclasses.

        Returns:
            The current data to be compared.
        """
        raise NotImplementedError("Subclasses must implement fetch_data method")

    def compare_data(self):
        """
        Compares previous and current data and triggers change events.
        This method should be overridden by subclasses to handle specific change detection logic.
        """
        raise NotImplementedError("Subclasses must implement compare_data method")


class DatabaseChangeDetector(ChangeDetector):
    def __init__(self, database, manager, check_interval=1):
        """
        Initializes the DatabaseChangeDetector instance.

        Args:
            database: An instance of the DataBase class.
            manager: The manager instance that handles database changes.
            check_interval: Time interval (in seconds) to check for changes.
        """
        super().__init__(check_interval)
        self.db = database
        self.manager = manager

    def fetch_data(self):
        """
        Fetches the current data from the database.

        Returns:
            A dictionary containing the current database records.
        """
        return self.db.findAll()  # Fetch current data from the database

    def compare_data(self):
        """
        Compares previous and current database data and logs the changes.
        """
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
                print("Modified record:")
                print(f"Previous: {previous_records[key]}")
                print(f"Current: {current_records[key]}")
                id = int(current_records[key]['arduino_parkplatz_id'])
                status = current_records[key]['status']
                special = bool(int(current_records[key]['spezial']))
                # Notify the manager about the database change
                self.manager.on_db_change(id, status, special)


class ArduinoChangeDetector(ChangeDetector):
    def __init__(self, arduino, manager, check_interval=1):
        """
        Initializes the ArduinoChangeDetector instance.

        Args:
            arduino: An instance of the Arduino or MockArduino class.
            manager: The manager instance that handles Arduino changes.
            check_interval: Time interval (in seconds) to check for changes.
        """
        super().__init__(check_interval)
        self.arduino = arduino
        self.manager = manager

    def fetch_data(self):
        """
        Fetches the current data from the Arduino.

        Returns:
            A list of dictionaries representing the status of each parking spot.
        """
        data = []
        anzahl_parkplaetze = self.arduino.getAnzahlParkplaetze()

        # Fetch status of each parking spot
        for parkplatz_id in range(anzahl_parkplaetze):
            occupied, reserved, special = self.arduino.getStatus(parkplatz_id)[1:]
            data.append({
                'parkplatz_id': parkplatz_id,
                'occupied': occupied,
                'reserved': reserved,
                'special': special
            })

        return data

    def compare_data(self):
        """
        Compares previous and current Arduino data and logs the changes.
        """
        for idx, current_record in enumerate(self.current_data):
            previous_record = self.previous_data[idx] if self.previous_data is not None else None

            if previous_record is None or previous_record != current_record:
                print("Modified Arduino record:")
                print(f"Previous: {previous_record}")
                print(f"Current: {current_record}")

                parkplatz_id = current_record['parkplatz_id']
                occupied = current_record['occupied']
                reserved = current_record['reserved']
                special = current_record['special']

                # Notify the manager about the Arduino change
                self.manager.on_arduino_change(parkplatz_id, occupied, reserved, special)
