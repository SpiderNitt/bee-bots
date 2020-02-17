#include "encoders.h"
#include <Arduino.h>

Encoders::Encoders(void (*fun1)(), void (*fun2)()) {
    pinMode(leftencoder,INPUT);
    pinMode(rightencoder,INPUT);

    attachInterrupt(digitalPinToInterrupt(leftencoder), fun1, RISING);
    attachInterrupt(digitalPinToInterrupt(rightencoder), fun2, RISING);
}

void Encoders::incrementleftticks()
{
    leftTicks++;
}

void Encoders::incrementrightticks()
{
    righTicks++;
}

void Encoders::computeRPM()
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