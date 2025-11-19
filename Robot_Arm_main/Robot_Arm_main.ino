#include <Stepper.h>

const int stepsPerRevolution = 200;  
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

// Enable pins for L298N
const int ENA = 5;
const int ENB = 6;

void setup() {
  Serial.begin(9600);
  
  // Enable the motor driver
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);
  
  myStepper.setSpeed(60); // Set speed to 60 RPM
  
  Serial.println("Use arrow keys: 'u' = up, 'd' = down");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'u') {
      myStepper.step(100); // move forward 100 steps
      Serial.println("Moved Up");
    }
    else if (command == 'd') {
      myStepper.step(-100); // move backward 100 steps
      Serial.println("Moved Down");
    }
  }
}