#ifndef PID_H

#define PID_H

class PID_ {
    double *current, *correction, *target;
    float kp, ki, kd;
    double errorSum, lastError;
    public:
    PID_ (double*, double*, double*, float, float, float);
    void Compute();
    void SetTunings(float, float, float);
    float GetKp();
    float GetKd();
    float GetKi();
};

#endif