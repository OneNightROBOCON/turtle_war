#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Control Your Turtlebot!
random walk. when pressed bunper, back and turn. then go ahead.
"""

speed = .2 
pressed_bumper = False
STATE = {'init':0, 'run':1, 'back':2, 'turn':3}
state = STATE['init']

def getBunperState():
    pressed_bumper = hogehoge
    return pressed_bumper

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('randam_walk')
    pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5)

    try:
        print msg
        while not rospy.is_shutdown():
            twist = Twist()
            twist.linear.x = speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            pub.publish(twist)

    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
