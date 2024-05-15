const int ledPin1 = 3;  // Pin for bulb 1
const int ledPin2 = 4;  // Pin for bulb 2
const int ledPin3 = 5;  // Pin for bulb 3

void setup() {
  Serial.begin(9600);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n'); // Read the entire message until newline character
    message.trim(); // Remove leading and trailing whitespace characters

    // First, turn off all LEDs to reset their states
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
        digitalWrite(6, LOW);
    digitalWrite(7, LOW);


    if (message.equals("L")) {
      // All lights are already off
      Serial.println("Done");
      return; // Exit the loop iteration
    } 

    if (message.startsWith("[") && message.endsWith("]")) {
      // Remove the brackets and parse the pin numbers
      message = message.substring(1, message.length() - 1);
      message.replace(" ", ""); // Remove all spaces
      int pin = message.toInt(); // Convert the first pin number

      // Handle cases where multiple pins are sent in the format [3,4,5]
      while (message.length() > 0) {
        int commaIndex = message.indexOf(',');
        if (commaIndex == -1) {
          pin = message.toInt();
          activatePin(pin);
          break; // No more commas, exit loop
        } else {
          pin = message.substring(0, commaIndex).toInt();
          activatePin(pin);
          message = message.substring(commaIndex + 1);
        }
      }
      
    }
      Serial.println("Done");
  }

}

void activatePin(int pin) {
  switch (pin) {
    case 3:
      digitalWrite(ledPin1, HIGH);
      break;
    case 4:
      digitalWrite(ledPin2, HIGH);
      break;
    case 5:
      digitalWrite(ledPin3, HIGH);
      break;
    case 6:
      digitalWrite(6, HIGH);
      break;
    case 7:
      digitalWrite(7, HIGH);
      break;
    case 8:
      digitalWrite(8, HIGH);
      break;
    case 9:
      digitalWrite(9, HIGH);
      break;
    default:
      // If the pin number is not recognized, do nothing
      break;
  }
}
