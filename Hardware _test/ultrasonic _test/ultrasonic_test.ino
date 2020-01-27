#define trigger 4
#define echo 7
 
float t=0,distance=0;
 
void setup()
{
 pinMode(trigger,OUTPUT);
 pinMode(echo,INPUT);
 Serial.begin(9600);
}
 
void loop()
{
 digitalWrite(trigger,LOW);
 delayMicroseconds(2);
 digitalWrite(trigger,HIGH);
 delayMicroseconds(8);
 digitalWrite(trigger,LOW);
 delayMicroseconds(2);
 t=pulseIn(echo,HIGH); 
 distance=((t*340)/20000);

 Serial.print(" Distance(in cm) :");
 Serial.println(distance);
}

