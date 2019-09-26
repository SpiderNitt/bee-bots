int MA1,MB1,MA2,MB2;
void setup() {
  pinMode(5,OUTPUT);    // Enable A
  pinMode(6,OUTPUT);    // Enable B
  
  pinMode(8,OUTPUT);    //IN1
  pinMode(9,OUTPUT);    //IN2
  
  pinMode(10,OUTPUT);   //IN3
  pinMode(11,OUTPUT);   //IN4

  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
 
  //forward direction 
  digitalWrite(8,LOW);      
  digitalWrite(9,HIGH);

  digitalWrite(10,LOW);
  digitalWrite(11,HIGH);
}

void loop() 
{
  MA1 = analogRead(A0); 
  MB1 = analogRead(A1);
  MA2 = analogRead(A2);
  MB2 = analogRead(A3);
  
  Serial.print(MA1);
  Serial.print(",");
  Serial.print(MB1);
  Serial.print(",");
  Serial.print(MA2);
  Serial.print(",");
  Serial.println(MB2);                    //open serial plotter
  
  
}
