#include <Stepper.h>

// Change these to match your stepper's characteristics.
const int stepsPerRevolution = 200;  
Stepper myStepper(stepsPerRevolution, 2, 3, 4, 5);

const int buttonUp = 8; // Connect "Up" button to digital pin 8
const int buttonDown = 9; // Connect "Down" button to digital pin 9

void setup() {
  pinMode(buttonUp, INPUT_PULLUP);
  pinMode(buttonDown, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(buttonUp) == LOW) {
    myStepper.step(1); // Move one step forward
  }
  if (digitalRead(buttonDown) == LOW) {
    myStepper.step(-1); // Move one step backward
  }
  // You may add delays as needed
}
