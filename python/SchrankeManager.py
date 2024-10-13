import time
from time import sleep

from Arduino import SchrankeArduino
from DataBase import DataBase, ParkplatzStatus
from SharedData import data_lock, shared_data


class SchrankeManager:
    def __init__(self, database: DataBase, schranke_arduino: SchrankeArduino):
        self.database = database
        self.schranke_arduino = schranke_arduino
        self.schranke_status = False

    def run(self):
        while True:
            self.database.setParkplatzToFreeIfOlderThan(10, time.time())
            status = self.schranke_arduino.getStatus()
            if status < 200 and not self.schranke_status:
                if self.updateShadredData():
                    self.schranke_status = True
                    self.schranke_arduino.setSchranke(True)
            else:
                self.schranke_status = False
                self.schranke_arduino.setSchranke(False)
            sleep(0.5)

    def updateShadredData(self):
        free = int(self.database.getFreeAmount()['records'][0]['total_free_parkplaetze'])
        amount = int(self.database.getTotalAmount()['records'][0]['total_parkplaetze'])
        find_next_spot = self.database.findNextSpot()['records']
        if len(find_next_spot) > 0:
            next_free_spot = find_next_spot[0]
            self.database.updateParkplatz(next_free_spot['key_id'], 0, next_free_spot['arduino_parkplatz_id'],
                                          ParkplatzStatus.RESERVIERT_SYSTEM.value, next_free_spot['spezial'])
            next_parking_spot = f"Nächster freier Parkplatz: Reihe {next_free_spot['reihe']} Nummer {next_free_spot['parkplatz_nummer']}"
            found_parking_stop = True
        else:
            next_parking_spot = f"Keine Parkplätze mehr verfügbar"
            found_parking_stop = False

        print("free", free)
        print("amount", amount)
        print("next_free_spot", next_parking_spot)

        with data_lock:
            shared_data['parking_spot_amount'] = amount
            shared_data['free'] = free
            shared_data[
                'next_parking_spot'] = next_parking_spot
        return  found_parking_stop
