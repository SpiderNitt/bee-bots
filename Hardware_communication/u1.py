#!/usr/bin/env python
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import rospy
from std_msgs.msg import String,Float32MultiArray,Float64

GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG = 07                                  #Associate pin 07 to TRIG
ECHO = 12                                  #Associate pin 12 to ECHO

print "Distance measurement in progress"


def dist():
	GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
	
	GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

	while True:

	  GPIO.output(TRIG, False)                 #Set TRIG as LOW
	  print "Waitng For Sensor To Settle"
	  time.sleep(2)                            #Delay of 2 seconds

	  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
	  time.sleep(0.00001)                      #Delay of 0.00001 seconds
	  GPIO.output(TRIG, False)                 #Set TRIG as LOW

	  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
	    pulse_start = time.time()              #Saves the last known time of LOW pulse

	  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
	    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

	  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

	  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
	  distance = round(distance, 2)            #Round to two decimal points

	  if distance > 2 and distance < 400:      #Check whether the distance is within range
	    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
	    return distance
	  else:
	    print "Out Of Range"                   #display out of range
	

	



def publish(ultra1):
    pub = rospy.Publisher('distance_send',Float64,queue_size=18)
    rospy.init_node('distance', anonymous=True)
    rospy.loginfo(ultra1)
    my_for_publishing = Float64(data=ultra1)
    pub.publish(my_for_publishing)
    

if __name__ == '__main__':
    try:
        ultra1 = dist()
        publish(ultra1)
    except rospy.ROSInterruptException:
        pass







