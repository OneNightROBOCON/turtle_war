#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import time

from geometry_msgs.msg import Twist

def callback(data):
	rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
	twist = Twist()
	twist.linear.x = control_speed
	twist.linear.y = 0
	twist.linear.z = 0
	twist.angular.x = 0
	twist.angular.y = 0
	twist.angular.z = control_turn
	self.vel_pub.publish(twist)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("chatter", String, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
