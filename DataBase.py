import os
import requests
from dotenv import load_dotenv

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

insert_sql = """
INSERT INTO parkplatz (reihe, parkplatz_nummer, arduino_id, arduino_parkplatz_id, status, spezial, zeitstempel)
VALUES (1, 101, 12345, 54321, 'Frei', 0, 1696672984);
"""

update_sql = """
UPDATE parkplatz
SET reihe = 2, 
    parkplatz_nummer = 102, 
    arduino_id = 67890, 
    arduino_parkplatz_id = 98765, 
    status = 'Besetzt', 
    spezial = 1, 
    zeitstempel = 1696679999
WHERE key_id = 1;
"""

# Load environment variables from the .env file
load_dotenv()


class DataBase:
    def __init__(self):
        self.url = os.getenv("PHP_SERVICE_URL")  # z.B. "https://voidtalk.de/B5_LF7/sql.php"

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

    def findAll(self):
        return self.formatResponse(self.sendSQL("SELECT * FROM `parkplatz`;"))

    def find(self, ID):
        return self.formatResponse(self.sendSQL(f"SELECT * FROM parkplatz WHERE key_id = {ID};"))

    def findWithArduinoID(self, arduinoID):
        return self.formatResponse(self.sendSQL(f"SELECT * FROM parkplatz WHERE arduino_id = {arduinoID};"))

    def findWithStatus(self, status):
        return self.formatResponse(
            self.sendSQL(f"SELECT * FROM parkplatz WHERE status = '{status}';"))  # Enclose status in quotes

    def newParkplatz(self, reihe, parkplatzNummer, arduinoID, arduinoParkplatzID, status, special, timestamp):
        return self.formatResponse(self.sendSQL(
            f"INSERT INTO parkplatz (reihe, parkplatz_nummer, arduino_id, arduino_parkplatz_id, status, spezial, zeitstempel) VALUES "
            f"({reihe}, {parkplatzNummer}, {arduinoID}, {arduinoParkplatzID}, '{status}', {str(special).upper()}, {timestamp});"
        ))  # Ensure proper formatting of the SQL statement

    def updateParkplatz(self, ID, reihe, parkplatzNummer, arduinoID, arduinoParkplatzID, status, special, timestamp):
        return self.formatResponse(self.sendSQL(
            f"UPDATE parkplatz SET reihe = {reihe}, parkplatz_nummer = {parkplatzNummer}, "
            f"arduino_id = {arduinoID}, arduino_parkplatz_id = {arduinoParkplatzID}, status = '{status}', spezial = {str(special).upper()}, "
            f"zeitstempel = {timestamp} WHERE key_id = {ID};"
        ))  # Ensure proper formatting of the SQL statement

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
