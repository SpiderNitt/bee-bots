#pragma once

#include <PID_v1.h>

class Pid
{

    double Set_rpm ; 
    double pidRightCorrection,pidLeftCorrection;
    PID pidright;
    PID pidleft;
        
    public :
    Pid(float Kpl=1,float Kil=9,float Kdl=0.01,float Kpr=1,float Kir=8,float Kdr=0.01,double set_rpm=100.0,double *rrpm = 0,double *lrpm = 0);


    //void pid_init();

    double pid_right();
    double pid_left();
    void pid_set_right(float kpl,float kil,float kdl);
    void pid_set_left(float kpr,float kir,float kdr);
    void set_motor_rpm(double rpm);
    void compute();
};