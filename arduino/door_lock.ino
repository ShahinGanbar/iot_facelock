
#include <Servo.h>

// Define the servo pin (change this to match your wiring)
const int SERVO_PIN = 9;  // Usually PWM capable pin
Servo doorLock;  // Create servo object
String inputString = "";  // String to hold incoming data

void setup() {
  // Start serial communication
  Serial.begin(9600);
  inputString.reserve(200);  // Reserve space for input string
  
  // Attach servo to pin
  doorLock.attach(SERVO_PIN);
  
  // Initialize to locked position
  doorLock.write(0);
  delay(1000);  // Give the servo time to reach position
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      // Convert string to integer
      int angle = inputString.toInt();
      // Ensure angle is within valid range
      angle = constrain(angle, 0, 180);
      // Move servo to position
      doorLock.write(angle);
      // Send confirmation
      Serial.print("Moved to angle: ");
      Serial.println(angle);
      // Clear the string for next time
      inputString = "";
    } else {
      inputString += inChar;
    }
  }
}
