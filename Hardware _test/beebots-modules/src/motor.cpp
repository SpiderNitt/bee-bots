#include "motor.h"
#include <Arduino.h>


Motor::Motor() 
{
    pinMode(leftdir, OUTPUT);
    pinMode(leftpwm, OUTPUT);

    pinMode(rightdir, OUTPUT);
    pinMode(rightpwm, OUTPUT);

    leftSpeed = rightSpeed = 0;
    stopped = true;
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
	digitalWrite(rightdir, LOW);
    stopped = false;
}

void Motor::leftturn()
{
    lpos=BACK;
    rpos=FRONT;
    digitalWrite(leftdir,HIGH);
    digitalWrite(rightdir,LOW);
    stopped = false;
}

void Motor::rightturn()
{
    lpos=FRONT;
    rpos=BACK;
    digitalWrite(leftdir,LOW);
    digitalWrite(rightdir,HIGH);
    stopped = false;
}

void Motor::brake()
{
    lpos=STOP;
    rpos=STOP;
    digitalWrite(leftdir,LOW);
    digitalWrite(rightdir,LOW);
    stopped = true;
}


void Motor::setleftspeed(unsigned int left)
{
    leftSpeed = min(255, left);
    if (!stopped) analogWrite(leftpwm,leftSpeed);
    else analogWrite(leftpwm, 0);
}

void Motor::setrightspeed(unsigned int right)
{
    rightSpeed = min(255, right);
    if (!stopped) analogWrite(rightpwm,rightSpeed);
    else analogWrite(rightpwm, 0);
}

void Motor::addToLeftSpeed(int l) {
    leftSpeed += l;
    if (leftSpeed > 255)
        leftSpeed = 255;
    if (!stopped) analogWrite(leftpwm,leftSpeed);
    else analogWrite(leftpwm, 0);
}

void Motor::addToRightSpeed(int r) {
    rightSpeed += r;
    if (rightSpeed > 255)
        rightSpeed = 255;
    analogWrite(rightpwm,rightSpeed);
    if (!stopped) analogWrite(rightpwm,rightSpeed);
    else analogWrite(rightpwm, 0);
}

unsigned int Motor::getLeftVoltage() {
    return (!stopped) ? leftSpeed: 0;
}

unsigned int Motor::getRightVoltage() {
    return (!stopped) ? rightSpeed: 0;
}
