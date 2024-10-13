class Parkplatz {
private:
  int specialPin;  // Reihe des Parkplatzes
  int reservePin;  // Nummer des Parkplatzes

public:
  bool spezialParkplatz = false;
  bool reserviert = false;

  // Konstruktor
  Parkplatz(int specialPin, int reservePin)
    : specialPin(specialPin), reservePin(reservePin) {}

  Parkplatz(int specialPin, int reservePin, bool spezialParkplatz, bool reserviert)
    : specialPin(specialPin), reservePin(reservePin) {
    spezialParkplatz = spezialParkplatz;
    reserviert = reserviert;
  }

  // Getter für die Reihe
  int getSpecialPin() const {
    return specialPin;
  }

  // Getter für die Parkplatznummer
  int getReservePin() const {
    return reservePin;
  }

  bool getIsSpezialParkplatz() {
    return spezialParkplatz;
  }

  bool getIsReserviert() {
    return reserviert;
  }

  setIsSpezialParkplatz(bool spezialParkplatz) {
    this->spezialParkplatz = spezialParkplatz;
  }

  setIsReserviert(bool reserviert) {
    this->reserviert = reserviert;
  }
};


//Parkplätze
Parkplatz parkplaetze[] = {
  Parkplatz(13, 12),
  Parkplatz(11, 10)
};


int anzahlParkplaetze = sizeof(parkplaetze) / sizeof(parkplaetze[0]);

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB
  }
  pinMode(LED_BUILTIN, OUTPUT);

  for (int i = 0; i <= anzahlParkplaetze; ++i) {
    pinMode(parkplaetze[i].getReservePin(), OUTPUT);
    pinMode(parkplaetze[i].getSpecialPin(), OUTPUT);
  }
}

void loop() {
  programm();
}

void programm() {
  if (Serial.available() > 0) {
    String input = Serial.readString();

    if (input == "ANZAHL PARKPLAETZE") {
      Serial.println(String(anzahlParkplaetze));
    } else {
      String command = input.substring(1, input.length());
      int id = atoi(input.substring(0, 1).c_str());

      if (id < anzahlParkplaetze) {
        computeCommand(id, command);
      } else {
        Serial.println("NOT A VALID ID");
      }
    }
  }
}

String boolToString(bool Bool) {
  return (Bool ? "true" : "false");
}

void computeCommand(int id, String command) {
  Parkplatz &parkplatz = parkplaetze[id];

  if (command == "RESERVE ON") {
    parkplatz.setIsReserviert(true);
    Serial.println(String(id) + boolToString(parkplatz.getIsReserviert()));
    digitalWrite(parkplatz.getReservePin(), HIGH);
  } else if (command == "RESERVE OFF") {
    parkplatz.setIsReserviert(false);
    Serial.println(String(id) + boolToString(parkplatz.getIsReserviert()));
    digitalWrite(parkplatz.getReservePin(), LOW);

  } else if (command == "STATUS") {
    Serial.println(String(id) + (boolToString(digitalRead(parkplatz.getReservePin()))) + (boolToString(parkplatz.getIsReserviert())) + (boolToString(parkplatz.getIsSpezialParkplatz())));

  } else if (command == "SPECIAL ON") {
    parkplatz.setIsSpezialParkplatz(true);
    Serial.println(String(id) + boolToString(parkplatz.getIsSpezialParkplatz()));
    digitalWrite(parkplatz.getSpecialPin(), HIGH);
  } else if (command == "SPECIAL OFF") {
    parkplatz.setIsSpezialParkplatz(false);
    Serial.println(String(id) + boolToString(parkplatz.getIsSpezialParkplatz()));
    digitalWrite(parkplatz.getSpecialPin(), LOW);
  } else {
    Serial.println("NOT A VALID COMMAND");
  }
}