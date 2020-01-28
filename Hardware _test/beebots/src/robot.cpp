#include "robot.h"
#include <Arduino.h>

#define POSITION_COMPUTE_INTERVAL 150

robot::robot(void(*fun)(),void(*fun2)()):
motor(fun,fun2)
{
    float posX = 0 , posY = 0  , orientation = 0  ;
    float targetPosX = 0  , targetPosY = 0  , targetOrientation = 0  , finalOrientation = 0;
    float currentDistance  = 0, targetDistance  = 0 ;

    arm.attach(2);
    arm.write(0);
}

void robot::updatePosition()
{
    float wheelRadius = radius;
	float axleLength = length;

	static float prevTime = micros();
	float deltaTime = (micros() - prevTime) / 1000000.0f;
	float rpm = (motor.lrpm + motor.rrpm) / 2;

	float distanceTravelled = (motor.lpos + motor.rpos) / 2 * deltaTime * rpm * wheelRadius * 2 * PI;
	float angleTurned = (motor.rpos - motor.lpos) / 2 * deltaTime * rpm * 2 * PI / 60;
	float angle = angleTurned * wheelRadius * 2 / axleLength;
	currentDistance += distanceTravelled;

	orientation += angle;
	if (orientation > 2 * PI)
		orientation -= 2 * PI;
	else if (orientation < 0)
		orientation += 2 * PI;
	posX += cos(orientation) * distanceTravelled;
	posY += sin(orientation) * distanceTravelled;

	prevTime = micros();
}

void robot::findAngle()
{
	targetOrientation = atan((targetPosY - posY) / (targetPosX - posX));

	if ((targetPosY - posY) == 0) //X-Axis
	{
		if (targetPosX - posX > 0)
			targetOrientation = 0;
		else
			targetOrientation = PI;
	}
	else if ((targetPosX - posX) == 0) //Y-Axis
	{
		if (targetPosY - posY > 0)
			targetOrientation = PI/2;
		else
			targetOrientation = 0.75 * PI;
	}
	else if (((targetPosY - posY) > 0) && ((targetPosX - posX) > 0)) // 1st QUADRANT
		targetOrientation = targetOrientation;
	else if (((targetPosY - posY) > 0) && ((targetPosX - posX) < 0)) // 2nd QUADRANT
		targetOrientation += PI;
	else if (((targetPosY - posY) < 0) && ((targetPosX - posX) < 0)) // 3rd QUADRANT
		targetOrientation += PI;
	else if (((targetPosY - posY) < 0) && ((targetPosX - posX) > 0)) // 4th QUADRANT
		targetOrientation += 2 * PI;

	if (targetOrientation > 2 * PI)
		targetOrientation -= 2 * PI;

	if (targetOrientation < 0)
		targetOrientation += 2 * PI;
}

void robot::setTarget(float x, float y, float o)
{
	targetPosX = x;
	targetPosY = y;
	finalOrientation = o;
	findAngle();
	targetDistance = distanceToTarget();
	currentDistance = 0;

	currentState = TURNING_TO_FACE_TARGET;
}

float robot::distanceToTarget() {
	return sqrt(square(posY - targetPosY) - square(posX - targetPosX));
} 

void robot::control() {
    pid.compute();

    motor.setleftspeed(pid.pid_left());
    motor.setrightspeed(pid.pid_right());

    static unsigned long prevComputeTime = millis();
    if (millis() - prevComputeTime > POSITION_COMPUTE_INTERVAL)
	{
		motor.computeRPM();
		prevComputeTime = millis();
	}

    updatePosition();

    switch (currentState)
	{
	case TURNING_TO_FACE_TARGET:

		Serial.print(orientation);
		Serial.print("\t");
		Serial.println(targetOrientation);

		if (abs(orientation - targetOrientation) > 0.1)
		{
			motor.leftturn();
		}
		else {
			motor.brake();
			currentState = MOVING_TOWARDS_TARGET;
		}
		break;
	case MOVING_TOWARDS_TARGET:
		if (currentDistance < targetDistance) {
			motor.forward();
		}
		else {
			motor.brake();
			currentState = IDLE;
		}
		break;
	}

	static int angle = 0;

	if (Serial.available()) {
		char c = Serial.read();
		switch(c) {
			case '1':
				setTarget(0, 10, PI/2);
			break;
			case 's':
				angle = max(angle-10, 0);
				arm.write(angle);

    Serial.println(angle);
			break;
			case 'a':
				angle = min(angle+10, 180);
				arm.write(angle);

    Serial.println(angle);
			break;
            case 'f':
                motor.forward();
                break;
		}
	}
    Serial.print(motor.lrpm);
    Serial.print("\t");
    Serial.print(motor.rrpm);
    Serial.print("\t");
    Serial.print(pid.pid_left());
    Serial.print("\t");
    Serial.println(pid.pid_right());

    delay(10);
}