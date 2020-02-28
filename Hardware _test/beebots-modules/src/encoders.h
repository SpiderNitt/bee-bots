#ifndef ENCODERS_H
#define ENCODERS_H

class Encoders {
    typedef int pin;

    const pin RENC = 19;
    const pin LENC = 21;

#ifdef LEFTMOTOR_A
    const pin &leftencoder = LENC;
    const pin &rightencoder = RENC;
#else
    const pin &leftencoder = RENC;
    const pin &rightencoder = LENC;
#endif

    const float TICKS_PER_REV = 3690.0;
    
    public:
    double lrpm;
    double rrpm;
    volatile unsigned leftTicks;
    volatile unsigned righTicks;
    Encoders(void (*)(), void (*)());
    void incrementleftticks();
    void incrementrightticks();
    void computeRPM();
};

#endif