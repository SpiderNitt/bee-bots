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
    const pin RENC = 18;
    const pin LENC = 19;

    

    const float TICKS_PER_REV = 3690.0;

    //bool enabled;

#ifdef LEFTMOTOR_A
    const pin &leftFront = AIN1;
    const pin &rightFront = BIN1;

    const pin &leftBack = AIN2;
    const pin &rightBack = BIN2;

    const pin &leftSpeed = PWMA;
    const pin &rightSpeed = PWMB;
    const pin &leftencoder = LENC;
    const pin &rightencoder = RENC;
#else
    const pin &leftFront = BIN1;
    const pin &rightFront = AIN1;

    const pin &leftBack = BIN2;
    const pin &rightBack = AIN2;

    const pin &leftSpeed = PWMB;
    const pin &rightSpeed = PWMA;
    const pin &leftencoder = RENC;
    const pin &rightencoder = LENC;
#endif

public:
    float lrpm;
    float rrpm;
    volatile unsigned leftTicks;
    volatile unsigned righTicks;
    enum Direction {STOP=0,FRONT=1,BACK=-1};

    Direction lpos = STOP;
    Direction rpos = STOP;

    Motor(void(*fun)(), void(*fun2)());
    //void setup();
    void forward();
    void reverse();
    void leftturn();
    void rightturn();
    void brake();
    void computeRPM();
    void incrementleftticks();
    void incrementrightticks();
    void setleftspeed(int);
    void setrightspeed(int);
    void attachinterrupt(void(*fun)(), void(*fun2)());

};

#endif