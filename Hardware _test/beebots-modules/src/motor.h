#ifndef MOTOR_DRIVER_INTERFACE_H
#define MOTOR_DRIVER_INTERFACE_H

#include <stdint.h>

//change A with B to swap left and right motors
#define LEFTMOTOR_B

class Motor {
    //pin definitions
    typedef int pin;
    
    //const pin STBY = 13;
    const pin PWMA = 11;
    const pin AIN2 = 34;
    const pin AIN1 = 33;
    const pin BIN1 = 35;
    const pin BIN2 = 36;
    const pin PWMB = 12;

#ifdef LEFTMOTOR_A
    const pin &leftFront = AIN1;
    const pin &rightFront = BIN1;

    const pin &leftBack = AIN2;
    const pin &rightBack = BIN2;

    const pin &leftSpeed = PWMA;
    const pin &rightSpeed = PWMB;
#else
    const pin &leftFront = BIN1;
    const pin &rightFront = AIN1;

    const pin &leftBack = BIN2;
    const pin &rightBack = AIN2;

    const pin &leftSpeed = PWMB;
    const pin &rightSpeed = PWMA;
#endif

public:
    enum Direction {STOP=0,FRONT=1,BACK=-1};

    Direction lpos = STOP;
    Direction rpos = STOP;

    Motor();
    void forward();
    void reverse();
    void leftturn();
    void rightturn();
    void brake();
    void setleftspeed(int);
    void setrightspeed(int);
};

#endif
