#define Pi 3.141592
float x_cur , y_cur  ;
float x_set , y_set  ;
float cur_theta ;
float set_theta ;
float req_theta ;
float control ; 
void set_angle()
{ set_theta = 180*atan( (y_set - y_cur)/(x_set - x_cur) )/Pi;

 
  if((y_set - y_cur) == 0)                            //X-Axis
  { if(x_set - x_cur > 0)
        set_theta = 0;
    else
        set_theta = 180;
  }
  else 
  if((x_set - x_cur) == 0)                            //Y-Axis
  { if(y_set - y_cur>0)  
        set_theta = 90 ;
    else
        set_theta = 270 ; 
  }
  else
  if(((y_set - y_cur) > 0) && ((x_set - x_cur) > 0))  // 1st QUADRANT  
    set_theta  = set_theta ;
  else 
  if(((y_set - y_cur) > 0) && ((x_set - x_cur) < 0))  // 2nd QUADRANT  
    set_theta  += 180;
  else
  if(((y_set - y_cur) < 0) && ((x_set - x_cur) < 0))  // 3rd QUADRANT 
   set_theta   += 180;
  else
  if(((y_set - y_cur) < 0) && ((x_set - x_cur) > 0))   // 4th QUADRANT 
   set_theta   += 360;

}
void setup() {
  Serial.begin(9600);
  Serial.print("enter x_cur :");
  x_cur = Serial.parseFloat();
  Serial.print("enter y_cur :");
  y_cur = Serial.parseFloat();
  Serial.print("enter x_set :");
  x_set = Serial.parseFloat();
  Serial.print("enter y_set :");
  y_set = Serial.parseFloat();
  Serial.print("enter cur_theta");
  cur_theta = Serial.parseFloat();
  set_angle();
  
  if(set_theta>  180)
    control = 'l';
  else
  if(set_theta < 180)
    control = 'r';
  
  
  
  }

void loop() {
Serial.println("direction of rotation :");
Serial.println(control);
Serial.println("angle turn required (degrees) :");
Serial.println(set_theta);
delay(1000);
}
