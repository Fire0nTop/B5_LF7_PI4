import os
import time  # Import time to get the current timestamp
from enum import Enum

import requests
from dotenv import load_dotenv


class ParkplatzStatus(Enum):
    FREI = "Frei"
    BESETZT = "Besetzt"
    RESERVIERT_SYSTEM = "Reserviert (System)"
    RESERVIERT_ADMIT = "Reserviert (Admit)"
    DEAKTIVIERT = "Deaktiviert"

    @staticmethod
    def get_status(occupied: bool = None, reserved: bool = None, fromAdmin: bool = None, status_str: str = None):
        # Check if both a status string and booleans are provided, which would be inconsistent
        if status_str is not None and (occupied is not None or reserved is not None or fromAdmin is not None):
            raise ValueError("Cannot provide both a status string and boolean flags.")

        # Handle the case where status is provided as a string
        if status_str is not None:
            status_str = status_str.lower()
            if status_str == "frei":
                return ParkplatzStatus.FREI
            elif status_str == "besetzt":
                return ParkplatzStatus.BESETZT
            elif status_str == "reserviert (system)":
                return ParkplatzStatus.RESERVIERT_SYSTEM
            elif status_str == "reserviert (admit)":
                return ParkplatzStatus.RESERVIERT_ADMIT
            elif status_str == "deaktiviert":
                return ParkplatzStatus.DEAKTIVIERT
            else:
                raise ValueError(f"Invalid status string: {status_str}")

        # Fallback to boolean checks if string is not provided
        if occupied is None or reserved is None:
            raise ValueError("Occupied and reserved flags must be provided if no status string is given.")

        if not occupied and not reserved:
            return ParkplatzStatus.FREI
        elif occupied and not reserved:
            return ParkplatzStatus.BESETZT
        elif reserved and occupied and not fromAdmin:
            return ParkplatzStatus.RESERVIERT_SYSTEM
        elif reserved and occupied and fromAdmin:
            return ParkplatzStatus.RESERVIERT_ADMIT
        else:
            return ParkplatzStatus.DEAKTIVIERT

    @staticmethod
    def get_flags(status: 'ParkplatzStatus'):
        if status == ParkplatzStatus.FREI:
            return False, False  # occupied, reserved
        elif status == ParkplatzStatus.BESETZT:
            return True, False  # occupied, reserved
        elif status == ParkplatzStatus.RESERVIERT_SYSTEM or status == ParkplatzStatus.RESERVIERT_ADMIT:
            return True, True  # occupied, reserved
        elif status == ParkplatzStatus.DEAKTIVIERT:
            return False, True  # No active states
        else:
            raise ValueError("Invalid ParkplatzStatus value")


create_table_sql = """
CREATE TABLE parkplatz (
    key_id INT AUTO_INCREMENT PRIMARY KEY,       -- Primary Key with auto-increment
    reihe INT NOT NULL,                          -- Row number (int)
    parkplatz_nummer INT NOT NULL,               -- Parking spot number (int)
    arduino_id INT NOT NULL,                     -- Arduino ID (int)
    arduino_parkplatz_id INT NOT NULL,           -- Arduino parking spot ID (int)
    status ENUM('Frei', 'Besetzt', 'Reserviert (System)', 'Reserviert (Admit)', 'Deaktiviert') NOT NULL, -- Enum for status
    spezial TINYINT(1) NOT NULL,                 -- Special flag (tinyint)
    zeitstempel BIGINT NOT NULL                  -- Timestamp (bigint)
);
"""

# Load environment variables from the .env file
load_dotenv()


class DataBase:
    def __init__(self):
        self.url = os.getenv("PHP_SERVICE_URL")  # e.g., "https://voidtalk.de/B5_LF7/sql.php"

    def sendSQL(self, query):
        """Sends an SQL query and returns the JSON response."""
        try:
            response = requests.post(self.url, data={'query': query})
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            return response.json()  # Return the decoded JSON response

        except requests.exceptions.RequestException as e:
            print(f"Error sending SQL query: {e}")
            return None
        except ValueError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def formatResponse(self, response):
        """Formats the response JSON into a simple, readable format."""
        if response and isinstance(response, list) and len(response) > 0:
            formatted = []
            for record in response:
                formatted.append({key: value for key, value in record.items()})
            return formatted
        elif response and isinstance(response, dict):
            return {key: value for key, value in response.items()}
        else:
            print("No records found in the response.")
            return []

    def getCurrentTimestamp(self):
        """Returns the current timestamp."""
        return int(time.time())

    def findAll(self):
        return self.formatResponse(self.sendSQL("SELECT * FROM `parkplatz`;"))

    def find(self, ID):
        return self.formatResponse(self.sendSQL(f"SELECT * FROM parkplatz WHERE key_id = {ID};"))

    def findWithArduinoID(self, arduinoID):
        return self.formatResponse(self.sendSQL(f"SELECT * FROM parkplatz WHERE arduino_id = {arduinoID};"))

    def findWithStatus(self, status):
        return self.formatResponse(
            self.sendSQL(f"SELECT * FROM parkplatz WHERE status = '{status}';"))  # Enclose status in quotes

    def newParkplatz(self, reihe, parkplatzNummer, arduinoID, arduinoParkplatzID, status, special):
        timestamp = self.getCurrentTimestamp()
        return self.formatResponse(self.sendSQL(
            f"INSERT INTO parkplatz (reihe, parkplatz_nummer, arduino_id, arduino_parkplatz_id, status, spezial, zeitstempel) VALUES "
            f"({reihe}, {parkplatzNummer}, {arduinoID}, {arduinoParkplatzID}, '{status}', {str(special).upper()}, {timestamp});"
        ))  # Ensure proper formatting of the SQL statement

    def updateParkplatzWithReiheAndNummer(self, ID, reihe, parkplatzNummer, arduinoID, arduinoParkplatzID, status,
                                          special):
        timestamp = self.getCurrentTimestamp()
        return self.formatResponse(self.sendSQL(
            f"UPDATE parkplatz SET reihe = {reihe}, parkplatz_nummer = {parkplatzNummer}, "
            f"arduino_id = {arduinoID}, arduino_parkplatz_id = {arduinoParkplatzID}, status = '{status}', spezial = {str(special).upper()}, "
            f"zeitstempel = {timestamp} WHERE key_id = {ID};"
        ))  # Ensure proper formatting of the SQL statement

    def updateParkplatz(self, ID, arduinoID, arduinoParkplatzID, status, special):
        timestamp = self.getCurrentTimestamp()
        return self.formatResponse(self.sendSQL(
            f"UPDATE parkplatz SET "
            f"arduino_id = {arduinoID}, arduino_parkplatz_id = {arduinoParkplatzID}, "
            f"status = '{status}', spezial = {str(special).upper()}, zeitstempel = {timestamp} "
            f"WHERE key_id = {ID};"
        ))

    def reSetupTabel(self):
        dropResponse = self.sendSQL("DROP TABLE IF EXISTS parkplatz;")
        createResponse = self.sendSQL(
            "CREATE TABLE parkplatz ("
            "key_id INT AUTO_INCREMENT PRIMARY KEY, "
            "reihe INT NOT NULL, "
            "parkplatz_nummer INT NOT NULL, "
            "arduino_id INT NOT NULL, "
            "arduino_parkplatz_id INT NOT NULL, "
            "status ENUM('Frei', 'Besetzt', 'Reserviert (System)', 'Reserviert (Admit)', 'Deaktiviert') NOT NULL, "
            "spezial BOOLEAN NOT NULL, "
            "zeitstempel BIGINT NOT NULL);"
        )
        return dropResponse, createResponse

    def findWithArduinoAndParkplatzID(self, arduinoID, parkplatzID):
        """Find a parking spot by arduino_id and arduino_parkplatz_id."""
        return self.formatResponse(self.sendSQL(
            f"SELECT * FROM parkplatz WHERE arduino_id = {arduinoID} AND arduino_parkplatz_id = {parkplatzID};"
        ))

    def setParkplatzToFreeIfOlderThan(self, timeDifference, givenTimestamp):
        """Sets all parkplätze with status 'Reserviert (System)' to 'Frei'
           and 'spezial' equal to 0 if their timestamp is less than the given timestamp."""
        query = f"""
        UPDATE parkplatz
        SET status = 'Frei'
        WHERE zeitstempel < {givenTimestamp - timeDifference}
        AND status = 'Reserviert (System)'
        AND spezial = 0;
        """
        return self.formatResponse(self.sendSQL(query))

    def findNextSpot(self):
        return self.formatResponse(self.sendSQL(
            f"SELECT * FROM parkplatz WHERE status = 'Frei' ORDER BY reihe ASC, parkplatz_nummer ASC LIMIT 1"
        ))

    def getTotalAmount(self):
        return self.formatResponse(self.sendSQL(
            f"SELECT COUNT(*) AS total_parkplaetze FROM parkplatz;"
        ))

    def getFreeAmount(self):
        return self.formatResponse(self.sendSQL(
            f"SELECT COUNT(*) AS total_free_parkplaetze FROM parkplatz WHERE status = 'Frei';"
        ))

    def setParkplatzToFreeIfOlderThan(self, timeDifference, givenTimestamp):
        """Sets all parkplätze with status 'Reserviert (System)' to 'Frei'
           if their timestamp is less than the given timestamp."""
        query = f"""
        UPDATE parkplatz
        SET status = 'Frei'
        WHERE zeitstempel < {givenTimestamp - timeDifference}
        AND status = 'Reserviert (System)';
        """
        return self.formatResponse(self.sendSQL(query))

