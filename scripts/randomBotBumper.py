#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random

from abstractBot import *
from geometry_msgs.msg import Twist

class RandomBot(AbstractBot):

    STATES = {"init":0, "straight":1, "back":2, "turn":3}
    state = STATES['init']
    timer = 0

    def strategy(self):
        pass

    def gazeboCallback(self, data):
        control_speed = 0.8
        control_turn = 1.

        if self.state == self.STATES['init']:
            self.state = self.STATES['straight']

        twist = Twist()
        twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn

        if self.state == self.STATES['straight']:
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            if self.bumper.state == 1:
                self.state = self.STATES['back']
                self.bumper.state = 0
                self.timer = 200

        elif self.state == self.STATES['back']:
            twist.linear.x = -control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 
            self.timer -= 1
            if self.timer < 0:
                self.state = self.STATES['turn']
                self.timer = 3000

        elif self.state == self.STATES['turn']:
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
            self.timer -= 1
            if self.timer < 0:
                self.state = self.STATES['straight']

        else:
            # err
            pass

        self.vel_pub.publish(twist)

if __name__ == '__main__':
    rospy.init_node('random_bot')

    bot = RandomBot('Random')

    rospy.spin()

