#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String,Float32MultiArray

def publish(point):
    pub = rospy.Publisher('velocity',Float32MultiArray,queue_size=10)
    rospy.init_node('velocity', anonymous=True)
    rospy.loginfo(point)
    pub.publish(point)
    

if __name__ == '__main__':
    try:
        point=[1,1]
        publish(point)
    except rospy.ROSInterruptException:
        pass