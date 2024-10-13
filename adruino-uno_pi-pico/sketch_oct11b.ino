// Constants
const int pResistor = 26;
const int lightthreshold = 200;

// Variables
int lightvalue;
int timeDelay = 3000;
bool schrankeState = false;  // false = closed, true = open

void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);
  while (!Serial) {;}
  
  // Step motor pins
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  
  // Stepmotor Starting state
  digitalWrite(0, HIGH);
  digitalWrite(1, LOW);
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(10);
  
  // Light Resistor
  pinMode(pResistor, INPUT);
}

void loop() {
  // Check if a command is available via Serial
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read the incoming serial data until newline
    
    if (input == "SCHRANKE ON") {
      if (schrankeState == false) {
        openSchranke();  // Call function to open the barrier
        schrankeState = true;  // Update state to open
      }
      Serial.println(schrankeState);  // Return the state (true)
    } else if (input == "SCHRANKE OFF") {
      if (schrankeState == true) {
        closeSchranke();  // Call function to close the barrier
        schrankeState = false;  // Update state to closed
      }
      Serial.println(schrankeState);  // Return the state (false)
    } else if (input == "STATUS") {
      // Read and send the light sensor value
      lightvalue = analogRead(pResistor);
      Serial.println(lightvalue);  // Return light sensor value
    }
  }
}

// Function to open the barrier
void openSchranke() {
  for (int i = 0; i < 102; i++) {  // Looping for a full rotation
    digitalWrite(3, LOW);
    digitalWrite(1, HIGH);
    delayMicroseconds(timeDelay);
    digitalWrite(0, LOW);
    digitalWrite(2, HIGH);
    delayMicroseconds(timeDelay);
    digitalWrite(1, LOW);
    digitalWrite(3, HIGH);
    delayMicroseconds(timeDelay);
    digitalWrite(2, LOW);
    digitalWrite(0, HIGH);
    delayMicroseconds(timeDelay);
  }
  
  digitalWrite(2, HIGH);
  digitalWrite(0, LOW);
  delayMicroseconds(timeDelay * 500);  // Delay to keep the barrier open
}

// Function to close the barrier
void closeSchranke() {
  for (int j = 0; j < 102; j++) {  // Looping for a full rotation in the other direction
    digitalWrite(3, LOW);
    digitalWrite(1, HIGH);
    delayMicroseconds(timeDelay);
    digitalWrite(0, HIGH);
    digitalWrite(2, LOW);
    delayMicroseconds(timeDelay);
    digitalWrite(1, LOW);
    digitalWrite(3, HIGH);
    delayMicroseconds(timeDelay);
    digitalWrite(2, HIGH);
    digitalWrite(0, LOW);
    delayMicroseconds(timeDelay);
  }
  
  digitalWrite(2, LOW);
  digitalWrite(0, HIGH);  // Prepare electromagnets to go the other direction
}
