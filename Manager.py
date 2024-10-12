import threading
import time

from Arduino import ParkplatzArduino, Arduino
from DatabaseChangeDetector import DatabaseChangeDetector
from ConsoleCommandInput import ConsoleCommandInput
from DataBase import ParkplatzStatus, DataBase
from SharedData import dataBaseChanges, data_lock


class Manager():
    def __init__(self):
        self.database = DataBase()
        self.parkplatz_arduino = ParkplatzArduino(Arduino.selectArduinoPort())

        # Console Input
        consoleInput = ConsoleCommandInput(self)
        consoleInput_thread = threading.Thread(target=consoleInput.run, daemon=True)
        consoleInput_thread.daemon = True
        consoleInput_thread.start()
        time.sleep(3)
        self.initDataBase()

        # Change detector for Database
        change_detector = DatabaseChangeDetector(self.database)
        detection_thread = threading.Thread(target=change_detector.detect_changes, daemon=True)
        detection_thread.daemon = True
        detection_thread.start()

    def run(self):
        while True:
            self.updateDbFromArduino()
            self.updateArduinosFromDb()
            time.sleep(1)

    def initDataBase(self):
        self.database.reSetupTabel()
        for parkplatz_id in range(self.parkplatz_arduino.getAnzahlParkplaetze()):
            _, occupied, reserved, special = self.parkplatz_arduino.getStatus(parkplatz_id)
            self.database.newParkplatz(0, 0, 0, parkplatz_id,
                                       ParkplatzStatus.get_status(occupied, reserved, False).value, special,
                                       time.time())

    def updateArduinosFromDb(self):
        with data_lock:
            if len(dataBaseChanges) > 0:
                change = dataBaseChanges.pop(0)
                print("old record", change['previous'])
                print("new record", change['current'])

                current_change = change['current']
                anzahl_parkplaetze = self.parkplatz_arduino.getAnzahlParkplaetze()
                parkplatz_id = int(current_change['arduino_parkplatz_id'])
                if parkplatz_id in range(anzahl_parkplaetze):
                    _, occupied, reserved, special = self.parkplatz_arduino.getStatus(parkplatz_id)
                    parkplatz_status = ParkplatzStatus.get_status(occupied, reserved, False)
                    current_status = current_change['status']
                    current_spezial = bool(int(current_change['spezial']))

                    if current_status == parkplatz_status.value and current_spezial == special:
                        print("not a valid change")
                    else:
                        _, reserved = ParkplatzStatus.get_flags(ParkplatzStatus.get_status(_, _, _, current_status))
                        self.parkplatz_arduino.setReserved(parkplatz_id, reserved)
                        self.parkplatz_arduino.setSpecial(parkplatz_id, current_spezial)

                else:
                    print("parkplatzId: ", parkplatz_id, " Out of range")

    def updateDbFromArduino(self):
        with data_lock:
            anzahl_parkplaetze = self.parkplatz_arduino.getAnzahlParkplaetze()
            for parkplatz_id in range(anzahl_parkplaetze):
                if len(dataBaseChanges) == 0:
                    _, occupied, reserved, special = self.parkplatz_arduino.getStatus(parkplatz_id)
                    key_id = int(self.database.findWithArduinoAndParkplatzID(0, parkplatz_id)['records'][0]['key_id'])
                    self.database.updateParkplatz(key_id, 0, parkplatz_id,
                                                  ParkplatzStatus.get_status(occupied, reserved, False).value, special)