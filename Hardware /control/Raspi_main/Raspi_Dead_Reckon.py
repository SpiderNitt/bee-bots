import serial
import math
import time
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM) 
#GPIO.setup(2, GPIO.OUT) 
#GPIO.setup(3, GPIO.OUT)
#GPIO.output(2, GPIO.LOW)
#GPIO.output(3, GPIO.LOW)

#set parameters and initial turn for now change when required
x = 0
y = 0
theta = 0
radius = 0.036       #radius of the wheel
L = 0.325
x_set = 3
y_set = 3
theta_set = 45
theta_set = theta_set*3.141592653589793/180
del_theta = 0
reset = 1     
ser = serial.Serial('COM18')
flush_value = ser.read(4)
control = 'l'
while(1):
    p = ser.read(4)
    q = ser.read(4)
    p.decode("utf-8")
    q.decode("utf-8")
    vl = float(p) + 0.00000000000001         #to make sure that both the velocites are not same in which case R will become infinity
    vr = float(q) 
    
    if(control == 'l'):
        vl=-vl
    elif(control == 'r'):
        vr=-vr
    
    R = (L*(vl+vr))/(2*(vr-vl))
    del_theta = (vr-vl)*0.05/L
              
    #odometry calculation type -1
    #ICC_x = x - R*math.sin(theta)
    #ICC_y = y + R*math.cos(theta) 
    #x = (math.cos(del_theta) - math.sin(del_theta))*(x-ICC_x) + ICC_x
    #y = (math.sin(del_theta) + math.cos(del_theta))*(y-ICC_y) + ICC_y

    #odometry calculation type -2
    left_delta = vl*0.05
    right_delta = vr*0.05
    if(abs(left_delta-right_delta)<0.02):
        x = x + left_delta*math.cos(theta)
        y = y + right_delta*math.sin(theta)        
    else:
        x = x + R*math.sin(theta+del_theta) - R*math.sin(theta)
        y = y - R*math.cos(theta+del_theta) + R*math.cos(theta)

    if(control == 'l'):
        theta = theta + del_theta
    elif(control == 'r'):
        theta = theta + del_theta
    
    #print(theta*180/3.141592653589793)
    #theta calculation works fine
    
    print(control)
    
    #print(theta*57.29577)
    #print("x : "  )
    #print(x)
    #print("y : "  )
  
    if(theta > 6.283185)  :                                                          #to keep the value of the theta within 0 and 2pi
        theta = theta - 6.283185
    elif(theta < 0):
        theta = 6.283185 - theta

    #control
    if(control == 'l'):
        if(abs(theta_set-theta) < 0.087):
            control = 'f'
            reset = 1
            print("turning done")
    elif(control == 'r'):
        if(abs(theta - set_theta) < 0.087):
            control = 'f'
            print("turning done")
    elif(control == 'f'):
        if(math.sqrt((x_set - x)**2 + (y_set - y)**2)<0.5 ):
           control ='s'
           print("straight motion done")
           print(x)
           print(y)
           print(theta)
           time.sleep(4)

    print(math.sqrt((x_set - x)**2 + (y_set - y)**2))

    if(check == 'r'):
        if reset == 1:
            GPIO.output(4, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(4, GPIO.HIGH)
            reset = 0
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.HIGH)
    elif(check == 'l'):
        if reset == 1:
            GPIO.output(4, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(4, GPIO.HIGH)
            reset = 0
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
    elif(check == 'f'):
        if reset == 1:
            GPIO.output(4, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(4, GPIO.HIGH)
            reset = 0
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
    elif(check == 's'):
        if reset == 1:
            GPIO.output(4, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(4, GPIO.HIGH)
            reset = 0
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)

    
    
