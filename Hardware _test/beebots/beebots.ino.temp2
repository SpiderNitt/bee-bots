#include "src/robot.h"

void leftTickHandle();
void rightTickHandle();

robot bee(leftTickHandle, rightTickHandle);

void setup() {
    Serial.begin(9600);
}

void loop() {
    bee.control();
}

void leftTickHandle() {
    bee.motor.incrementleftticks();
}

void rightTickHandle() {
    bee.motor.incrementrightticks();
}