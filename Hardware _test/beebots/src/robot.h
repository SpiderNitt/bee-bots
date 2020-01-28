#pragma once

#include "Motor.h"
#include "PID.h"

#include <Servo.h>

class robot
{
    const float radius = 0.036;
    const float length = 0.325;
    float posX , posY , orientation ;
    float targetPosX , targetPosY , targetOrientation , finalOrientation ;
    float currentDistance , targetDistance ;
    enum State
    {
        IDLE,
        TURNING_TO_FACE_TARGET,
        MOVING_TOWARDS_TARGET
    } currentState ;

    public :
    robot(void(*fun)(),void(*fun2)());
    Motor motor;
    Pid pid;
    Servo arm;


    void updatePosition();
    void findAngle();
    void setTarget(float x,float y,float o);
    float distanceToTarget();
    void  control();
};