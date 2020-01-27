#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG1 = 26                              
ECHO1 = 21                            

def dist():
	GPIO.setup(TRIG1,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO1,GPIO.IN)                   #Set pin as GPIO in

	while True:
	  GPIO.output(TRIG1, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor1 To Settle"
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
          if distance1 > 2 and distance1 < 400:      #Check whether the distance is within range
	    return distance1-0.5	
	  else:
	    print "Out Of Range"                    #display out of range
	
def publish(ultra1):
    pub = rospy.Publisher('u1_dist_send',Float64,queue_size=18)
    rospy.init_node('distance1', anonymous=True)
    rospy.loginfo(ultra1)
    my1_for_publishing = Float64(data=ultra1)
    pub.publish(my1_for_publishing)


if __name__ == '__main__':
    try:
	while True:
		ultra1 = dist()
	        publish(ultra1)
    except rospy.ROSInterruptException:
        pass
