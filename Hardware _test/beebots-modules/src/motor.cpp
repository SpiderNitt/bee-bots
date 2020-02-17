#include "motor.h"
#include <Arduino.h>


Motor::Motor() 
{
    pinMode(leftdir, OUTPUT);
    pinMode(leftpwm, OUTPUT);

    pinMode(rightdir, OUTPUT);
    pinMode(rightpwm, OUTPUT);
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
	digitalWrite(leftpwm, HIGH);
	digitalWrite(rightpwm, HIGH);
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
    digitalWrite(leftpwm,HIGH);
    digitalWrite(leftdir,HIGH);
    digitalWrite(rightpwm,HIGH);
    digitalWrite(rightdir,HIGH);

}


void Motor::setleftspeed(int left)
{
    analogWrite(leftpwm,left);
}

void Motor::setrightspeed(int right)
{
    analogWrite(rightpwm,right);
}




