#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG4 = 06                              
ECHO4 = 12                          
print "Distance measurement in progress"

def dist():
	GPIO.setup(TRIG4,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO4,GPIO.IN)                   #Set pin as GPIO in

	while True:
	  GPIO.output(TRIG4, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                             #Delay of 2 seconds

	  GPIO.output(TRIG4, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                       #Delay of 0.00001 seconds
	  GPIO.output(TRIG4, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO4)==0:               #Check whether the ECHO is LOW
	    pulse_start4 = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO3)==1:               #Check whether the ECHO is HIGH
	    pulse_end4 = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration4 = pulse_end4 - pulse_start4  #Get pulse duration to a variable

	  distance4 = pulse_duration4 * 17150        #Multiply pulse duration by 17150 to get distance
	  distance4 = round(distance4, 2)            #Round to two decimal points

	  if distance4 > 2 and distance4 < 400:      #Check whether the distance is within range
	    return distance4-0.5
	  else:
	    print "Out Of Range"                    #display out of range
	
def publish(ultra4):
    pub = rospy.Publisher('u4_dist_send',Float64,queue_size=18)
    rospy.init_node('distance4', anonymous=True)
    rospy.loginfo(ultra4)
    my4_for_publishing = Float64(data=ultra4)
    pub.publish(my4_for_publishing)
    

if __name__ == '__main__':
    try:
        ultra4 = dist()
        publish(ultra4)
    except rospy.ROSInterruptException:
        pass


