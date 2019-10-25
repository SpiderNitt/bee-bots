void setup() {
  pinMode(5,OUTPUT);    // Enable A
  pinMode(6,OUTPUT);    // Enable B
  
  pinMode(8,OUTPUT);    //IN1
  pinMode(9,OUTPUT);    //IN2
  
  pinMode(10,OUTPUT);   //IN3
  pinMode(11,OUTPUT);   //IN4

  
}

void loop() {
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
 
  //forward direction
  digitalWrite(8,LOW);      
  digitalWrite(9,HIGH);

  digitalWrite(10,LOW);
  digitalWrite(11,HIGH);

  //backward direction
  digitalWrite(8,HIGH);      
  digitalWrite(9,LOW);

  digitalWrite(10,HIGH);
  digitalWrite(11,LOW);


  
}
