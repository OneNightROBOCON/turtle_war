#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random

from abstractBot import *

from geometry_msgs.msg import Twist

class RandomBot(AbstractBot):
    
    def strategy(self):
    
        r = rospy.Rate(100)
        
        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        surplus = 0

        update = True

        while not rospy.is_shutdown():
            
            value = random.randint(0,1000)

            mod = 4
            if update:
                surplus = value%mod
                update = False
            
            if surplus == 0:
                x = 1
                th = 0

            elif surplus == 1:
                x = 0
                th = 3

            elif surplus == 2:
                x = 0
                th = -3
            else:
                x = 0
                th = 0

            target_speed = x
            target_turn = th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed
                update = True

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn
                update = True

            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
        
            
            self.vel_pub.publish(twist)

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('random_bot')

    bot = RandomBot('Random')

    bot.strategy()