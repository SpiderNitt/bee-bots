#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Float32MultiArray
import fun

def callback(data):
    global x
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if data.data ==  "ok" :
          if x==len(path1)-1:
            print(reached)
          else:
            send_array=[path1[x],path1[x+1],path1[x+2]]
            publish(send_array)
            fun.set_position(19999,send_array)
            x=x+3
    
def listener():
    rospy.Subscriber("acknowledge",String, callback)
    rospy.spin()

def publish(point):
    pub = rospy.Publisher('Path',Float32MultiArray,queue_size=10)
    rospy.loginfo(point)
    array = point
    my_array_for_publishing = Float32MultiArray(data=array)
    pub.publish(my_array_for_publishing)

def node_init():
    rospy.init_node('Path_acknowledge', anonymous=True)
 
    


if __name__ == '__main__':
    path1=fun.path([2,2,0],19999)
    print(path1)
    x=0
    node_init()
    listener()

