import threading
from http.client import responses

import serial.tools.list_ports
from time import sleep


class Arduino:
    def __init__(self, port):
        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 9600
        self.serialInst.port = port
        self.serialInst.open()
        self.serial_lock = threading.Lock()

    def sendCommand(self, command):
        with self.serial_lock:
            print(f"CMD: {command}")
            self.serialInst.write(command.encode('utf-8'))
            sleep(0.05)
            response = self.serialInst.readline().decode('utf-8').strip()  # Clean response
            print(f"RES: {response}")
        return response

    @staticmethod
    def selectArduinoPort():
        ports = serial.tools.list_ports.comports()
        choices = []
        print('PORT\tDEVICE\t\t\tMANUFACTURER')

        for index, value in enumerate(sorted(ports)):
            if value.hwid != 'n/a':
                choices.append(index)
                print(f"{index}\t{value.name}\t{value.manufacturer}")

        choice = -1
        while choice not in choices:
            answer = input("➜ Select your port: ")
            if answer.isnumeric() and int(answer) in choices:
                choice = int(answer)

        print(f'Selecting: {ports[choice].device}')
        return ports[choice].device

class SchrankeArduino(Arduino):
    def setSchranke(self,on):
        response = self.sendCommand(f"SCHRANKE {'ON' if on else 'OFF'}")
        return response == "true"

    def getStatus(self):
        response = self.sendCommand("STATUS")
        return int(response)

class ParkplatzArduino(Arduino):
    def setReserved(self, ID, on):
        response = self.sendCommand(f"{ID}RESERVE {'ON' if on else 'OFF'}")
        return response == f"{ID}true"

    def setSpecial(self, ID, on):
        response = self.sendCommand(f"{ID}SPECIAL {'ON' if on else 'OFF'}")
        return response == f"{ID}true"

    def getStatus(self, ID):
        response = self.sendCommand(f"{ID}STATUS").strip()

        # Parse the first character as the ID number
        num = int(response[0])
        remaining_response = response[1:]  # Get everything after the first character

        # Parse the 'occupied' status
        if remaining_response.startswith("true"):
            occupied = True
            remaining_response = remaining_response[4:]
        elif remaining_response.startswith("false"):
            occupied = False
            remaining_response = remaining_response[5:]
        else:
            raise ValueError("Unexpected response for occupied")

        # Parse the 'reserved' status
        if remaining_response.startswith("true"):
            reserved = True
            remaining_response = remaining_response[4:]
        elif remaining_response.startswith("false"):
            reserved = False
            remaining_response = remaining_response[5:]
        else:
            raise ValueError("Unexpected response for reserved")

        # Parse the 'special' status
        if remaining_response.startswith("true"):
            special = True
        elif remaining_response.startswith("false"):
            special = False
        else:
            raise ValueError("Unexpected response for special")

        return num, occupied, reserved, special

    def getAnzahlParkplaetze(self):
        response = self.sendCommand("ANZAHL PARKPLAETZE").strip()

        try:
            anzahl_parkplaetze = int(response)
        except ValueError:
            raise ValueError("Unexpected response for number of parking spots")

        return anzahl_parkplaetze
