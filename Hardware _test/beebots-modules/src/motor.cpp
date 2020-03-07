#include "motor.h"
#include <Arduino.h>


Motor::Motor() 
{
    pinMode(leftdir, OUTPUT);
    pinMode(leftpwm, OUTPUT);

    pinMode(rightdir, OUTPUT);
    pinMode(rightpwm, OUTPUT);

    leftSpeed = rightSpeed = 0;
}

void Motor::reverse()
{
    lpos = rpos = BACK;
	digitalWrite(leftdir, HIGH);
	digitalWrite(leftpwm, HIGH);
	digitalWrite(rightdir, HIGH);
	digitalWrite(rightpwm, HIGH);

}

void Motor::forward()
{
	lpos = rpos = FRONT;
	digitalWrite(leftdir, LOW);
    setleftspeed(255);
    setrightspeed(255);
	digitalWrite(rightdir, LOW);
}

void Motor::leftturn()
{
    lpos=BACK;
    rpos=FRONT;
    digitalWrite(leftpwm,HIGH);
    digitalWrite(leftdir,HIGH);
    digitalWrite(rightpwm,HIGH);
    digitalWrite(rightdir,LOW);
}

void Motor::rightturn()
{
    lpos=FRONT;
    rpos=BACK;
    digitalWrite(leftpwm,HIGH);
    digitalWrite(leftdir,LOW);
    digitalWrite(rightpwm,HIGH);
    digitalWrite(rightdir,HIGH);
}

void Motor::brake()
{
    lpos=STOP;
    rpos=STOP;
    digitalWrite(leftpwm,LOW);
    digitalWrite(leftdir,LOW);
    digitalWrite(rightpwm,LOW);
    digitalWrite(rightdir,LOW);
}


void Motor::setleftspeed(unsigned int left)
{
    leftSpeed = max(255, left);
    analogWrite(leftpwm,leftSpeed);
}

void Motor::setrightspeed(unsigned int right)
{
    rightSpeed = max(255, right);
    analogWrite(rightpwm,rightSpeed);
}

void Motor::addToLeftSpeed(int l) {
    leftSpeed += l;
    if (leftSpeed > 255)
        leftSpeed = 255;
    analogWrite(leftpwm,leftSpeed);
}

void Motor::addToRightSpeed(int r) {
    rightSpeed += r;
    if (rightSpeed > 255)
        rightSpeed = 255;
    analogWrite(rightpwm,rightSpeed);
}

unsigned int Motor::getLeftVoltage() {
    return leftSpeed;
}

unsigned int Motor::getRightVoltage() {
    return rightSpeed;
}
