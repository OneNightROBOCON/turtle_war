#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import time

from geometry_msgs.msg import Twist



def subpub_callback(data):
	
	
	control_speed = data.linear.x
	control_turn = data.angular.z
	if control_speed < -0.5:
			control_speed = -0.5
	elif control_speed > 0.5:
			control_speed = 0.5
	if control_turn < -3:
			control_turn = -3
	elif control_turn > 0.5:
			control_turn = 3

	vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
	twist = Twist()
	twist.linear.x = control_speed
	twist.linear.y = 0
	twist.linear.z = 0
	twist.angular.x = 0
	twist.angular.y = 0
	twist.angular.z = control_turn
	vel_pub.publish(twist)

def limitter():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/cmd_vel", Twist, subpub_callback)
	rospy.spin()

if __name__ == '__main__':
	limitter()
