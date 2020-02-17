#include <PID_v1.h>
#include <Arduino.h>
#include <Servo.h>

#define RADIUS 0.036
#define LENGTH 0.325
#define UINT_MAX 4294967295
#define TICKS_PER_REV 3690.0
#define ENCODER_LEFT_PIN 19
#define ENCODER_RIGHT_PIN 21
#define POSITION_COMPUTE_INTERVAL 150
#define SEND_INTERVAL 100
#define TARGET_RPM 150

bool set_;
int rm1 = 33, rm2 = 34, rme = 11, lm1 = 35, lm2 = 36, lme = 12;
int renc = 21, lenc = 19;
double set = 100, lrpm, rrpm;
int lpos, rpos;
double pidRightCorrection, pidLeftCorrection;
volatile unsigned int leftTicks, rightTicks;
double prevX = 0, prevY = 0;
volatile int inChar = 4;
unsigned long prevPositionComputeTime = 0, prevSendTime = 0;
int start = 0;

/*Position control*/
float posX = 0, posY = 0, orientation = 0;
float targetPosX = 0, targetPosY = 0, targetOrientation = 0, finalOrientation = 0;
float currentDistance = 0, targetDistance = 0;

Servo arm;

enum State
{
	IDLE,
	TURNING_TO_FACE_TARGET,
	MOVING_TOWARDS_TARGET
} currentState = IDLE;

/*Control Parameters */
float Kpl = 1, Kil = 9, Kdl = 0.01; ///left
float Kpr = 1, Kir = 8, Kdr = 0.01; //right
float p_el = 0, p_er = 0;
float sm_el = 0, sm_er = 0;
int out_max = 255, out_min = 0;

PID pidRight(&rrpm, &pidRightCorrection, &set, Kpr, Kir, Kdr, DIRECT);
PID pidLeft(&lrpm, &pidLeftCorrection, &set, Kpl, Kil, Kdl, DIRECT);

void pulseLeft() { leftTicks++; }
void pulseRight() { rightTicks++; }

char states[][10] {
	"IDLE", 
	"TURNING",
	"MOVING"
};

void configureSET() {
	Serial.println("Enter SET: ");
	while(!Serial.available());
	set = Serial.readString().toFloat();	
}

void configureRightPID() {
	Serial.println("Enter KPR: ");
	while(!Serial.available());
	Kpr = Serial.readString().toFloat();

	Serial.println("Enter KDR: ");
	while(!Serial.available());
	Kdr = Serial.readString().toFloat();

	Serial.println("Enter KIR: ");
	while(!Serial.available());
	Kir = Serial.readString().toFloat();

	Serial.print("Setting values: ");
	Serial.print(Kpr);
	Serial.print(", ");
	Serial.print(Kdr);
	Serial.print(", ");
	Serial.print(Kir);
	Serial.print("\n");

	pidRight.SetTunings(Kpr, Kdr, Kir);
}

void configureLeftPID() {
	Serial.println("Enter KPL: ");
	while(!Serial.available());
	Kpl = Serial.readString().toFloat();

	Serial.println("Enter KDL: ");
	while(!Serial.available());
	Kdl = Serial.readString().toFloat();

	Serial.println("Enter KIL: ");
	while(!Serial.available());
	Kil = Serial.readString().toFloat();

	Serial.print("Setting values: ");
	Serial.print(Kpl);
	Serial.print(", ");
	Serial.print(Kdl);
	Serial.print(", ");
	Serial.print(Kil);
	Serial.print("\n");

	pidLeft.SetTunings(Kpl, Kdl, Kil);
}

void setup()
{

	Serial.begin(9600);
	float flusher = 3.14;
	pinMode(rm1, OUTPUT);
	pinMode(rm2, OUTPUT);
	pinMode(rme, OUTPUT);
	pinMode(lm1, OUTPUT);
	pinMode(lm2, OUTPUT);
	pinMode(lme, OUTPUT);
	pinMode(ENCODER_RIGHT_PIN, INPUT);
	pinMode(ENCODER_LEFT_PIN, INPUT);
	attachInterrupt(digitalPinToInterrupt(ENCODER_RIGHT_PIN), pulseRight, RISING);
	attachInterrupt(digitalPinToInterrupt(ENCODER_LEFT_PIN), pulseLeft, RISING);

	// configureRightPID();

	pidRight.SetMode(AUTOMATIC);
	pidLeft.SetMode(AUTOMATIC);

	arm.attach(2);
	arm.write(0);

	forward();
}

void forward()
{
	lpos = rpos = 1;
	digitalWrite(lm1, HIGH);
	digitalWrite(lm2, LOW);
	digitalWrite(rm1, HIGH);
	digitalWrite(rm2, LOW);
}

void reverse()
{
	lpos = rpos = -1;
	digitalWrite(lm2, HIGH);
	digitalWrite(lm1, LOW);
	digitalWrite(rm2, HIGH);
	digitalWrite(rm1, LOW);
}

void leftturn()
{
	lpos = -1;
	rpos = 1;
	digitalWrite(lm2, HIGH);
	digitalWrite(lm1, LOW);
	digitalWrite(rm1, HIGH);
	digitalWrite(rm2, LOW);
}

void rightturn()
{
	rpos = -1;
	lpos = 1;
	digitalWrite(lm1, HIGH);
	digitalWrite(lm2, LOW);
	digitalWrite(rm2, HIGH);
	digitalWrite(rm1, LOW);
}

void brake()
{
	lpos = rpos = 0;
	digitalWrite(lm1, HIGH);
	digitalWrite(lm2, HIGH);
	digitalWrite(rm2, HIGH);
	digitalWrite(rm1, HIGH);
}

unsigned long getElapsedTime(unsigned long prevTime)
{
	unsigned long currentTime = micros();
	if (currentTime < prevTime)
		return UINT_MAX - prevTime + currentTime;
	return currentTime - prevTime;
}

void updatePosition()
{
	float wheelRadius = RADIUS;
	float axleLength = LENGTH;

	static float prevTime = micros();
	float deltaTime = (micros() - prevTime) / 1000000.0f;
	float rpm = (lrpm + rrpm) / 2;

	float distanceTravelled = (lpos + rpos) / 2 * deltaTime * rpm * wheelRadius * 2 * PI;
	float angleTurned = (rpos - lpos) / 2 * deltaTime * rpm * 2 * PI / 60;
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

void printPosition()
{
	Serial.print(states[currentState]);
	Serial.print(":\t");
	Serial.print(posX);
	Serial.print("\t");
	Serial.print(posY);
	Serial.print("\t");
	Serial.println(orientation * 180 / PI);
}

void findAngle()
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

void setTarget(float x, float y, float o)
{
	targetPosX = x;
	targetPosY = y;
	finalOrientation = o;
	findAngle();
	targetDistance = distanceToTarget();
	currentDistance = 0;

	currentState = TURNING_TO_FACE_TARGET;
}

void computeRPM()
{
	static unsigned long prevTime = millis();
	float elapsedTime = (millis() - prevTime) / 1000.0f;
	if (elapsedTime > 0)
	{
		lrpm = leftTicks * 60.0f / (TICKS_PER_REV * elapsedTime);
		rrpm = rightTicks * 60.0f / (TICKS_PER_REV * elapsedTime);
	}

	prevTime = millis();
	leftTicks = 0;
	rightTicks = 0;
}

float distanceToTarget() {
	return sqrt(square(posY - targetPosY) - square(posX - targetPosX));
} 

void loop()
{
	pidRight.Compute();
	pidLeft.Compute();

	pidRightCorrection = round(pidRightCorrection);
	pidLeftCorrection = round(pidLeftCorrection);

	analogWrite(lme, pidRightCorrection);
	analogWrite(rme, pidLeftCorrection);

	if (millis() - prevPositionComputeTime > POSITION_COMPUTE_INTERVAL)
	{
		computeRPM();
		prevPositionComputeTime = millis();
	}

	updatePosition();
	//printPosition();
	

	switch (currentState)
	{
	case TURNING_TO_FACE_TARGET:

		Serial.print(orientation);
		Serial.print("\t");
		Serial.println(targetOrientation);

		if (abs(orientation - targetOrientation) > 0.1)
		{
			leftturn();
		}
		else {
			brake();
			currentState = MOVING_TOWARDS_TARGET;
		}
		break;
	case MOVING_TOWARDS_TARGET:
		if (currentDistance < targetDistance) {
			forward();
		}
		else {
			brake();
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
			case '0':
				angle = max(angle-10, 0);
				arm.write(angle);
			break;
			case '2':
				angle = min(angle+10, 180);
				arm.write(angle);
			break;
		}
	}

	// Serial.print("lrpm: ");
	// Serial.print(lrpm);
	// Serial.print("\t\t");
	// Serial.print("rrpm: ");
	// Serial.print(rrpm);

	// Serial.print("\t");
	// Serial.print(leftTicks);
	// Serial.print("\t");
	// Serial.println(pidRightCorrection);
	// Serial.println(angle);

	//Serial.print(states[currentState]);
	//Serial.print("\t");
	//Serial.print(orientation);
	//Serial.print("/");
	//Serial.print(targetOrientation);
	//Serial.print("\t");
	//Serial.print(currentDistance);
	//Serial.print("/");
	//Serial.print(targetDistance);
	//Serial.print("\n");
	Serial.println((lrpm + rrpm)/2);

	delay(10);
}
