class MockParkplatz:
    """Mock class to simulate a parking spot."""

    def __init__(self, specialPin, reservePin, spezialParkplatz=False, reserviert=False):
        self.specialPin = specialPin
        self.reservePin = reservePin
        self.spezialParkplatz = spezialParkplatz
        self.reserviert = reserviert

    def setIsSpezialParkplatz(self, spezialParkplatz):
        self.spezialParkplatz = spezialParkplatz

    def setIsReserviert(self, reserviert):
        self.reserviert = reserviert

    def getIsSpezialParkplatz(self):
        return self.spezialParkplatz

    def getIsReserviert(self):
        return self.reserviert


class MockArduino:
    """Mock class to simulate Arduino communication."""

    def sendCommand(self, command):
        """Mock sending a command to the Arduino and receiving a response."""
        print(f"Mock CMD: {command}")
        if command == "ANZAHL PARKPLAETZE":
            return str(len(self.parkplaetze))
        else:
            try:
                id = int(command[0])  # Extract the ID
                cmd = command[1:].strip()  # Extract the rest of the command

                if cmd == "STATUS":
                    return self.getStatus(id)
                elif "RESERVE" in cmd:
                    return self.handleReserveCommand(id, cmd)
                elif "SPECIAL" in cmd:
                    return self.handleSpecialCommand(id, cmd)
                else:
                    return "NOT A VALID COMMAND"
            except (ValueError, IndexError):
                return "INVALID COMMAND"

    def handleReserveCommand(self, id, command):
        """Mock handling RESERVE ON/OFF commands."""
        parkplatz = self.parkplaetze[id]
        if command == "RESERVE ON":
            parkplatz.setIsReserviert(True)
            return f"{id}true"
        elif command == "RESERVE OFF":
            parkplatz.setIsReserviert(False)
            return f"{id}false"
        else:
            return "INVALID RESERVE COMMAND"

    def handleSpecialCommand(self, id, command):
        """Mock handling SPECIAL ON/OFF commands."""
        parkplatz = self.parkplaetze[id]
        if command == "SPECIAL ON":
            parkplatz.setIsSpezialParkplatz(True)
            return f"{id}true"
        elif command == "SPECIAL OFF":
            parkplatz.setIsSpezialParkplatz(False)
            return f"{id}false"
        else:
            return "INVALID SPECIAL COMMAND"

    def getStatus(self, id):
        """Mock getting the status of a parking spot."""
        parkplatz = self.parkplaetze[id]
        reserved_status = "true" if parkplatz.getIsReserviert() else "false"
        special_status = "true" if parkplatz.getIsSpezialParkplatz() else "false"
        # Simulating the read state of the reserve pin as always "false" in this mock
        reserve_pin_state = "false"
        return f"{id}{reserve_pin_state}{reserved_status}{special_status}"


class MockParkplatzArduino(MockArduino):
    """Mock class to simulate ParkplatzArduino behavior."""

    def __init__(self):
        # Initialize parking spots like the real Arduino does
        self.parkplaetze = [
            MockParkplatz(13, 12),
            MockParkplatz(11, 10)
        ]

    def setReserved(self, ID, on):
        """Simulate setting a parking spot as reserved."""
        response = self.sendCommand(f"{ID}RESERVE {'ON' if on else 'OFF'}")
        return response == f"{ID}true"

    def setSpecial(self, ID, on):
        """Simulate setting a parking spot as special."""
        response = self.sendCommand(f"{ID}SPECIAL {'ON' if on else 'OFF'}")
        return response == f"{ID}true"

    def getStatus(self, ID):
        """Simulate getting the status of a parking spot."""
        # Use the existing getStatus method of MockArduino to avoid recursion
        response = super().getStatus(ID).strip()

        # Extracting and parsing the status
        num = int(response[0])
        remaining_response = response[1:]

        occupied = remaining_response[0:4] == "true"
        reserved = remaining_response[4:8] == "true"
        special = remaining_response[8:] == "true"

        return num, occupied, reserved, special

    def getAnzahlParkplaetze(self):
        """Simulate getting the number of parking spots."""
        response = self.sendCommand("ANZAHL PARKPLAETZE")
        return int(response)

    @staticmethod
    def selectArduinoPort():
        """Simulate selecting an Arduino port (mocked)."""
        return "/dev/mock_arduino"
