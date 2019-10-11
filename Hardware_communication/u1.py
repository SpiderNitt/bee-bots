#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG1 = 26                              
ECHO1 = 21
TRIG2 = 19                              
ECHO2 = 20
TRIG3 = 13                              
ECHO3 = 16
TRIG4 = 06                              
ECHO4 = 12
                                
print "Distance measurement in progress"

def dist():
	GPIO.setup(TRIG1,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO1,GPIO.IN)                   #Set pin as GPIO in
	GPIO.setup(TRIG2,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO2,GPIO.IN)                   #Set pin as GPIO in
	GPIO.setup(TRIG3,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO3,GPIO.IN)                   #Set pin as GPIO in
	GPIO.setup(TRIG4,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO4,GPIO.IN)                   #Set pin as GPIO in

	while True:

	  GPIO.output(TRIG1, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                             #Delay of 2 seconds

	  GPIO.output(TRIG1, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                       #Delay of 0.00001 seconds
	  GPIO.output(TRIG1, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO1)==0:               #Check whether the ECHO is LOW
	    pulse_start1 = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO1)==1:               #Check whether the ECHO is HIGH
	    pulse_end1 = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration1 = pulse_end1 - pulse_start1  #Get pulse duration to a variable

	  distance1 = pulse_duration1 * 17150        #Multiply pulse duration by 17150 to get distance
	  distance1 = round(distance1, 2)            #Round to two decimal points

    


`
	  GPIO.output(TRIG2, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                             #Delay of 2 seconds

	  GPIO.output(TRIG2, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                       #Delay of 0.00001 seconds
	  GPIO.output(TRIG2, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO2)==0:               #Check whether the ECHO is LOW
	    pulse_start2 = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO2)==1:               #Check whether the ECHO is HIGH
	    pulse_end2 = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration2 = pulse_end2 - pulse_start2  #Get pulse duration to a variable

	  distance2 = pulse_duration2 * 17150        #Multiply pulse duration by 17150 to get distance
	  distance2 = round(distance2, 2)            #Round to two decimal points



	  GPIO.output(TRIG3, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                             #Delay of 2 seconds

	  GPIO.output(TRIG3, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                       #Delay of 0.00001 seconds
	  GPIO.output(TRIG3, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO3)==0:               #Check whether the ECHO is LOW
	    pulse_start3 = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO3)==1:               #Check whether the ECHO is HIGH
	    pulse_end3 = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration3 = pulse_end3 - pulse_start3  #Get pulse duration to a variable

	  distance3 = pulse_duration3 * 17150        #Multiply pulse duration by 17150 to get distance
	  distance3 = round(distance3, 2)            #Round to two decimal points



	  GPIO.output(TRIG4, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                             #Delay of 2 seconds

	  GPIO.output(TRIG4, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                       #Delay of 0.00001 seconds
	  GPIO.output(TRIG4, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO4)==0:               #Check whether the ECHO is LOW
	    pulse_start4 = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO4)==1:               #Check whether the ECHO is HIGH
	    pulse_end4 = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration4 = pulse_end4 - pulse_start4  #Get pulse duration to a variable

	  distance4 = pulse_duration4 * 17150        #Multiply pulse duration by 17150 to get distance
	  distance4 = round(distance4, 2)            #Round to two decimal points


          if distance1 > 2 and distance1 < 400 and distance2 > 2 and distance2 < 400 and distance3 > 2 and distance3 < 400 and distance4 > 2 and distance4 < 400: #Check whether the distance is within range
	    return distance1-0.5
	    #return distance2-0.5
            #return distance3-0.5
	    #return distance4-0.5
	
	  else:
	    print "Out Of Range"                   #display out of range


	
def publish(ultra1):
    pub1 = rospy.Publisher('u1_dist_send',Float64,queue_size=18)
    rospy.init_node('distance1', anonymous=True)
    rospy.loginfo(ultra1)
    my1_for_publishing = Float64(data=ultra1)
    pub1.publish(my1_for_publishing)
    

if __name__ == '__main__':
    try:
        ultra1 = dist()
        publish(ultra1)
    except rospy.ROSInterruptException:
        pass







