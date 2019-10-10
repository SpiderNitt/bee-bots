
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import rospy
from std_msgs.msg import String

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.OUT)

p = GPIO.PWM(40, 50)

p.start(7.5)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if data.data == "pick":
       pick()
    elif data.data == "place":
       place()



def listener():

    rospy.init_node('servo', anonymous=True)

    rospy.Subscriber("servo", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def pick():
        p.ChangeDutyCycle(12.5) # turn towards 180 degree
        time.sleep(1) # sleep 1 second 

def place():

        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second

if __name__ == '__main__':
    
    listener()
