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
    const pin AIN2 = 10;
    //const pin AIN1 = 33;
    //const pin BIN1 = 35;
    const pin BIN2 = 3;
    const pin PWMB = 9;

#ifdef LEFTMOTOR_A
    //const pin &leftFront = AIN1;
    //const pin &rightFront = BIN1;

    const pin &leftdir = AIN2;
    const pin &rightdir = BIN2;

    const pin &leftpwm = PWMA;
    const pin &rightpwm = PWMB;
#else
    //const pin &leftFront = BIN1;
    //const pin &rightFront = AIN1;

    const pin &leftdir = BIN2;
    const pin &rightdir = AIN2;

    const pin &leftpwm = PWMB;
    const pin &rightpwm = PWMA;
#endif

public:
    enum Direction {STOP=0,FRONT=1,BACK=-1};

    Direction lpos = STOP;
    Direction rpos = STOP;

    int leftSpeed;
    int rightSpeed;

    Motor();
    void forward();
    void reverse();
    void leftturn();
    void rightturn();
    void brake();
    void setleftspeed(unsigned int);
    void setrightspeed(unsigned int);
    void addToLeftSpeed(int l);
    void addToRightSpeed(int r);
    unsigned int getLeftVoltage();
    unsigned int getRightVoltage();
};

#endif
