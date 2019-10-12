#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG3 = 13                              
ECHO3 = 16                           

def dist():
	GPIO.setup(TRIG3,GPIO.OUT)                  #Set pin as GPIO out	
	GPIO.setup(ECHO3,GPIO.IN)                   #Set pin as GPIO in

	while True:
	  GPIO.output(TRIG3, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor3 To Settle"
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

	  if distance3 > 2 and distance3 < 400:      #Check whether the distance is within range
	    return distance3-0.5
	  else:
	    print "Out Of Range"                    #display out of range
	
def publish(ultra3):
    pub = rospy.Publisher('u3_dist_send',Float64,queue_size=18)
    rospy.init_node('distance3', anonymous=True)
    rospy.loginfo(ultra3)
    my3_for_publishing = Float64(data=ultra3)
    pub.publish(my3_for_publishing)
    

if __name__ == '__main__':
    try:
        ultra3 = dist()
        publish(ultra3)
    except rospy.ROSInterruptException:
        pass
