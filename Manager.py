import threading
import time
from time import sleep

from Arduino import ParkplatzArduino, Arduino, SchrankeArduino
from ChangeDetector import DatabaseChangeDetector, ArduinoChangeDetector
from ConsoleCommandInput import ConsoleCommandInput
from DataBase import ParkplatzStatus, DataBase
from SchrankeManager import SchrankeManager
from SharedData import dataBaseChanges, data_lock

import threading
import time
from queue import Queue


class Manager():
    def __init__(self):
        self.database = DataBase()
        print("parkplatz")
        self.parkplatz_arduino = ParkplatzArduino(Arduino.selectArduinoPort())
        print("schranke")
        self.schranke_arduino = SchrankeArduino(Arduino.selectArduinoPort())

        self.update_queue = Queue()
        self.lock = threading.Lock()
        self.last_update_time = 0  # To track the last update timestamp

        # Initial State
        sleep(3)
        self.initDataBase()

        # Console Input
        consoleInput = ConsoleCommandInput(self)
        consoleInput_thread = threading.Thread(target=consoleInput.run, daemon=True)
        consoleInput_thread.daemon = True
        consoleInput_thread.start()

        # Initialize DatabaseChangeDetector
        self.db_change_detector = DatabaseChangeDetector(self.database, self)
        db_change_thread = threading.Thread(target=self.db_change_detector.detect_changes, daemon=True)
        db_change_thread.start()

        # Initialize ParkplatzChangeDetector
        self.arduino_change_detector = ArduinoChangeDetector(self.parkplatz_arduino, self)
        arduino_change_thread = threading.Thread(target=self.arduino_change_detector.detect_changes, daemon=True)
        arduino_change_thread.start()

        # Initialize SchrankeManager
        self.schranke_manager = SchrankeManager(self.database,self.schranke_arduino)
        schranke_manager_thread = threading.Thread(target=self.schranke_manager.run, daemon=True)
        schranke_manager_thread.start()

    def run(self):
        while True:
            self.process_updates()
            time.sleep(1)

    def initDataBase(self):
        self.database.reSetupTabel()
        for parkplatz_id in range(self.parkplatz_arduino.getAnzahlParkplaetze()):
            _, occupied, reserved, special = self.parkplatz_arduino.getStatus(parkplatz_id)
            self.database.newParkplatz(0, 0, 0, parkplatz_id,
                                       ParkplatzStatus.get_status(occupied, reserved, False).value, special)

    def process_updates(self):
        with self.lock:
            while not self.update_queue.empty():
                update = self.update_queue.get()
                self.handle_update(update)

    def handle_update(self, update):
        update_time, source, parkplatz_id, status, special = update

        # Check if this update is newer
        if update_time <= self.last_update_time:
            print("Ignored outdated update.")
            return

        if source == 'arduino':
            self.handle_arduino_update(parkplatz_id, status, special)
        elif source == 'database':
            self.handle_database_update(parkplatz_id, status, special)

        # Update the last update time
        self.last_update_time = update_time

    def handle_arduino_update(self, parkplatz_id, status, special):
        print(f"Updating database from Arduino for Parkplatz {parkplatz_id}: {status}, Special: {special}")
        # Get the corresponding key_id from the database
        key_id = self.database.findWithArduinoAndParkplatzID(0, parkplatz_id)['records'][0]['key_id']

        # Update the database with Arduino's status
        self.database.updateParkplatzWithReiheAndNummer(
            key_id,
            0,  # Assuming reihe is not needed here
            parkplatz_id,
            0,  # Arduino ID
            parkplatz_id,
            status,
            special  # Optional: use the current time as a timestamp
        )

    def handle_database_update(self, parkplatz_id, status, special):
        print(f"Updating Arduino from Database for Parkplatz {parkplatz_id}: {status}, Special: {special}")
        # Update Arduino's state based on database changes
        print(status)
        occupied, reserved = ParkplatzStatus.get_flags(ParkplatzStatus.get_status(None,None,None,status))
        self.parkplatz_arduino.setReserved(parkplatz_id, reserved)
        self.parkplatz_arduino.setSpecial(parkplatz_id, special)

    def updateFromArduino(self, parkplatz_id, status, special):
        # Push updates from Arduino into the queue
        self.update_queue.put((time.time(), 'arduino', parkplatz_id, status, special))

    def updateFromDatabase(self, parkplatz_id, status, special):
        # Push updates from Database into the queue
        self.update_queue.put((time.time(), 'database', parkplatz_id, status, special))

    def updateDbFromArduino(self):
        with self.lock:
            anzahl_parkplaetze = self.parkplatz_arduino.getAnzahlParkplaetze()
            for parkplatz_id in range(anzahl_parkplaetze):
                if len(dataBaseChanges) == 0:
                    _, occupied, reserved, special = self.parkplatz_arduino.getStatus(parkplatz_id)
                    key_id = int(self.database.findWithArduinoAndParkplatzID(0, parkplatz_id)['records'][0]['key_id'])
                    # Enqueue an update to the database
                    self.updateFromDatabase(parkplatz_id, ParkplatzStatus.get_status(occupied, reserved, False).value,
                                            special)

    def on_db_change(self, parkplatz_id, status, special):
        print(f"Detected change in database for Parkplatz {parkplatz_id}: Status={status}, Special={special}")
        # Update Arduino based on the database changes
        self.update_arduino_from_db(parkplatz_id, status, special)

    def on_arduino_change(self, parkplatz_id, occupied, reserved, special):
        print(f"Detected change in Arduino for Parkplatz {parkplatz_id}: Occupied={occupied}, Reserved={reserved}, Special={special}")
        # Update Database based on the Arduino changes
        self.update_db_from_arduino(parkplatz_id, occupied, reserved, special)

    def update_arduino_from_db(self, parkplatz_id, status, special):
        # Translate status back to occupied, reserved flags and update Arduino
        occupied, reserved = ParkplatzStatus.get_flags(ParkplatzStatus.get_status(status_str=status))
        #self.parkplatz_arduino.setOccupied(parkplatz_id, occupied)
        self.parkplatz_arduino.setReserved(parkplatz_id, reserved)
        self.parkplatz_arduino.setSpecial(parkplatz_id, special)

    def update_db_from_arduino(self, parkplatz_id, occupied, reserved, special):
        # Translate Arduino status to database format and update DB
        status = ParkplatzStatus.get_status(occupied, reserved, False).value
        key_id = int(self.database.findWithArduinoAndParkplatzID(0, parkplatz_id)['records'][0]['key_id'])
        self.database.updateParkplatz(key_id, 0, parkplatz_id, status, special)
