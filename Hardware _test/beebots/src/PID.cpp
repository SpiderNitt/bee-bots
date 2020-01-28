
#include <PID_v1.h>
#include "PID.h"

Pid::Pid(float kpl,float kil,float kdl,float kpr,float kir,float kdr,double set_rpm,double *rrpm,double *lrpm):
pidright(rrpm,&pidRightCorrection,&set_rpm,kpr,kir,kdr,DIRECT),
pidleft(lrpm,&pidLeftCorrection,&set_rpm,kpl,kil,kdl,0)
{

    Set_rpm = set_rpm ;



    pidright.SetMode(AUTOMATIC);
    pidleft.SetMode(AUTOMATIC);


}

double Pid::pid_left()
{
    return pidLeftCorrection;
}

double Pid::pid_right()
{
    return pidRightCorrection;
}

void Pid::pid_set_left(float Kpl,float Kil,float Kdl)
{
    pidright.SetTunings(Kpl,Kil,Kdl);
}

void Pid::pid_set_right(float Kpr,float Kir,float Kdr)
{
    pidright.SetTunings(Kpr,Kir,Kdr);
}

void Pid::set_motor_rpm(double rpm)
{
    Set_rpm = rpm;

}

void Pid::compute() {
    pidright.Compute();
    pidleft.Compute();
}