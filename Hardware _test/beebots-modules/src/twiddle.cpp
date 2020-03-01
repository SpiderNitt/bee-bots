#include "twiddle.h"
#include "motor.h"
#include "encoders.h"

#include <stdlib.h>
#include <Arduino.h>

#include "PID.h"

#define PID_TUNING_ACCURACY 0.0001

void Twiddle::autoTune(double& rpm, double set, PID_& pid, double& correction, void (Motor::*setSpeed)(int), Motor* motor, Encoders &encoder) {
    
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
            pid.SetTunings(kp, kd, ki);
            for (int i = 0; i < 100; ++i) {
                pid.Compute();
                (motor->*setSpeed)(correction);
                encoder.computeRPM();
                delay(10);
            }            
            err = abs(set - rpm);
            Serial.print("error: ");
            Serial.println(err);

            if (err < best_err) {
                best_err = err;
                dp[i] *= 1.1;
            }
            else {
                *(parameters[i]) += dp[i];
                pid.SetTunings(kp, kd, ki);
                for (int i = 0; i < 100; ++i) {
                    pid.Compute();
                    (motor->*setSpeed)(correction);
                    encoder.computeRPM();
                    delay(10);
                }            
                err = abs(set - rpm);
                Serial.print("error: ");
                Serial.println(err);

                if (err < best_err) {
                    best_err = err;
                    dp[i] *= 1.1;
                }
                else {
                    *(parameters[i]) += dp[i];
                    pid.SetTunings(kp, kd, ki);
                    dp[i] *= 0.9;
                }
            }
        }
        sum = (dp[0] +dp[1] + dp[2]); 
        Serial.println(sum);
    }   
}