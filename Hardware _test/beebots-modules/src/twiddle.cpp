#include "twiddle.h"
#include "motor.h"

#include <PID_v1.h>
#include <stdlib.h>
#include <Arduino.h>

#define PID_TUNING_ACCURACY 0.0001

void Twiddle::autoTune(double& rpm, double set, PID& pid, double& correction, void (Motor::*setSpeed)(int), Motor* motor) {
    
    float best_err = abs(set - rpm);
    float err;

    double dp[3] = {1,1,1};
    double kp = pid.GetKp();
    double kd = pid.GetKd();
    double ki = pid.GetKi();

    double* parameters[] = {&kp, &kd, &ki};

    double sum = (dp[0] + dp[1]);
    while (sum > PID_TUNING_ACCURACY) {
        for (int i = 0; i < 2; i++) {
            *(parameters[i]) += dp[i];
            pid.SetTunings(kp, kd, ki, DIRECT);
            pid.Compute();
            (motor->*setSpeed)(correction);
            
            err = abs(set - rpm);
            if (err < best_err) {
                best_err = err;
                dp[i] *= 1.1;
            }
            else {
                *(parameters[i]) += dp[i];
                pid.Compute();
                (motor->*setSpeed)(correction);
                err = abs(set - rpm);

                if (err < best_err) {
                    best_err = err;
                    dp[i] *= 1.1;
                }
                else {
                    *(parameters[i]) += dp[i];
                    dp[i] *= 0.9;
                }
            }
        }
        sum = (dp[0] +dp[1] + dp[2]); 
        Serial.println(sum);
    }   
}