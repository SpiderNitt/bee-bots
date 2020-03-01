#include "PID.h"

PID_::PID_ (double* _current, double* _correction, double* _target, float _kp, float _ki, float _kd) 
:current(_current), correction(_correction), target(_target)
{
    SetTunings(_kp, _kd, _ki);
    errorSum = 0;
    lastError = 0;
}

void PID_::SetTunings(float _kp, float _kd, float _ki) {
    kp = _kp;
    kd = _kd;
    ki = _ki;
}

void PID_::Compute() {
    double error = (*current) - (*target);
    errorSum += error;
    float p = kp * (error);
    float d = kd * (error - lastError);
    float i = ki * errorSum;
    lastError = error;

    *correction = p + d + i;
}

float PID_::GetKp() {
    return kp;
}

float PID_::GetKd() {
    return kd;
}

float PID_::GetKi() {
    return ki;
}