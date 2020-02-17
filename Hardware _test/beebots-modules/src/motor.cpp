#include "motor.h"
#include <Arduino.h>


Motor::Motor() 
{
    pinMode(leftFront, OUTPUT);
    pinMode(leftBack, OUTPUT);
    pinMode(leftSpeed, OUTPUT);

    pinMode(rightFront, OUTPUT);
    pinMode(rightBack, OUTPUT);
    pinMode(rightSpeed, OUTPUT);
}

void Motor::reverse()
{
    lpos = rpos = BACK;
	digitalWrite(leftBack, HIGH);
	digitalWrite(leftFront, LOW);
	digitalWrite(rightBack, HIGH);
	digitalWrite(rightFront, LOW);

}

void Motor::forward()
{
	lpos = rpos = FRONT;
	digitalWrite(leftFront, HIGH);
	digitalWrite(leftBack, LOW);
	digitalWrite(rightFront, HIGH);
	digitalWrite(rightBack, LOW);
}

void Motor::leftturn()
{
    lpos=BACK;
    rpos=FRONT;
    digitalWrite(leftBack,HIGH);
    digitalWrite(leftFront,LOW);
    digitalWrite(rightFront,HIGH);
    digitalWrite(rightBack,LOW);
}

void Motor::rightturn()
{
    lpos=FRONT;
    rpos=BACK;
    digitalWrite(leftFront,HIGH);
    digitalWrite(leftBack,LOW);
    digitalWrite(rightBack,HIGH);
    digitalWrite(rightFront,LOW);
}

void Motor::brake()
{
    lpos=STOP;
    rpos=STOP;
    digitalWrite(leftFront,HIGH);
    digitalWrite(leftBack,HIGH);
    digitalWrite(rightBack,HIGH);
    digitalWrite(rightFront,HIGH);

}


void Motor::setleftspeed(int left)
{
    analogWrite(leftSpeed,left);
}

void Motor::setrightspeed(int right)
{
    analogWrite(rightSpeed,right);
}




