#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG2 = 19                              
ECHO2 = 20                            

def dist():
	GPIO.setup(TRIG2,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO2,GPIO.IN)                   #Set pin as GPIO in

	while True:
	  GPIO.output(TRIG2, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor2 To Settle"
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

	  if distance2 > 2 and distance2 < 400:      #Check whether the distance is within range
	    return distance2-0.5
	  else:
	    print "Out Of Range"                    #display out of range
	
def publish(ultra2):
    pub = rospy.Publisher('u2_dist_send',Float64,queue_size=18)
    rospy.init_node('distance2', anonymous=True)
    rospy.loginfo(ultra2)
    my2_for_publishing = Float64(data=ultra2)
    pub.publish(my2_for_publishing)
    

if __name__ == '__main__':
    try:
        ultra2 = dist()
        publish(ultra2)
    except rospy.ROSInterruptException:
        pass

