import threading

from Arduino import Arduino
from ChangeDetector import ChangeDetector
from DataBase import DataBase

db = DataBase()
change_detector = ChangeDetector(db)
arduino = "" # Arduino(Arduino.selectArduinoPort())

detection_thread = threading.Thread(target=change_detector.detect_changes, daemon=True)
detection_thread.start()

while True:
    command = input("cmd: ")

    match command:
        case "exit":
            quit(0)
        case "special":
            status = arduino.getStatus(0)
            _, _, _, special = status
            print("special: " + str(arduino.setSpecial(0, not special)))
        case"reserved":
            status = arduino.getStatus(0)
            _, _, reserved, _ = status
            print("reserved: " + str(arduino.setReserved(0, not reserved)))
        case _:
            print(arduino.sendCommand(command))