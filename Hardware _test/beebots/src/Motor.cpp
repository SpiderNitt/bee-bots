
#include "Motor.h"
#include <Arduino.h>


Motor::Motor(void(*fun)(),void(*fun2)()) 
{
    pinMode(leftFront, OUTPUT);
    pinMode(leftBack, OUTPUT);
    pinMode(leftSpeed, OUTPUT);

    pinMode(rightFront, OUTPUT);
    pinMode(rightBack, OUTPUT);
    pinMode(rightSpeed, OUTPUT);

    pinMode(leftencoder,INPUT);
    pinMode(rightencoder,INPUT);

    attachinterrupt(fun,fun2);
}

void Motor::attachinterrupt(void(*fun)(),void(*fun2)())
{
    attachInterrupt(digitalPinToInterrupt(leftencoder), fun, RISING);
	attachInterrupt(digitalPinToInterrupt(rightencoder), fun2, RISING);
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

void Motor::incrementleftticks()
{
    leftTicks++;
}

void Motor::incrementrightticks()
{
    righTicks++;
}

void Motor::setleftspeed(int left)
{
    analogWrite(leftSpeed,left);
}

void Motor::setrightspeed(int right)
{
    analogWrite(rightSpeed,right);
}

void Motor::computeRPM()
{
    static unsigned long prevTime = millis();
    float elapsedTime = (millis() - prevTime) / 1000.0f;
    if (elapsedTime>0)
    {
        lrpm = leftTicks * 60.0f / (TICKS_PER_REV * elapsedTime);
        rrpm = righTicks * 60.0f / (TICKS_PER_REV * elapsedTime);

    }

    prevTime = millis();
    leftTicks = 0;
    righTicks = 0;
}



