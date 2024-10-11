import threading
from time import sleep

from Arduino import Arduino
from ChangeDetector import ChangeDetector
from DataBase import DataBase
from SharedData import shared_data, data_lock


def programm():
    db = DataBase()
    change_detector = ChangeDetector(db)
    arduino = "" # Arduino(Arduino.selectArduinoPort())

    detection_thread = threading.Thread(target=change_detector.detect_changes, daemon=True)
    detection_thread.start()

    # Handle input commands in a loop
    while True:
        command = "" # input("cmd: ")
        with data_lock:
            shared_data['occupied'] += 1
            shared_data['free'] -= 1
            shared_data['next_parking_spot'] = f"P{shared_data['occupied'] + 1}"
        sleep(1)
        print(shared_data['free'])
        match command:
            case "exit":
                print("Exiting program...")
                break  # Exit the loop to end the programm
            case "special":
                status = arduino.getStatus(0)
                _, _, _, special = status
                print("special: " + str(arduino.setSpecial(0, not special)))
            case "reserved":
                status = arduino.getStatus(0)
                _, _, reserved, _ = status
                print("reserved: " + str(arduino.setReserved(0, not reserved)))
            case _:
                print("default")#arduino.sendCommand(command))

    print("Programm has ended.")
