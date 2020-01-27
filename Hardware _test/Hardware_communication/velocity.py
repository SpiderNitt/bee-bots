#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Float32MultiArray

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    rospy.init_node('velocity', anonymous=True)

    rospy.Subscriber("velocity", Float32MultiArray, callback)

    
    rospy.spin()

if __name__ == '__main__':
    listener()
