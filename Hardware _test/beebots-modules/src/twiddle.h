#ifndef TWIDDLE_H
#define TWIDDLE_H

#include "motor.h"
#include "encoders.h"
#include "PID.h"

namespace Twiddle {
    void autoTune(double& rpm, double set, PID_& pid, double& correction, void (Motor::*setSpeed)(int), Motor* motor, Encoders &encoder);
};


#endif