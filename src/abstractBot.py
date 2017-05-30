#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from geometry_msgs.msg import Twist
import rospy

class AbstractBot(object):
    __metaclass__ = ABCMeta
    def __init__(self,bot_name):
        self.name = bot_name
        self.vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)

    @abstractmethod
    def strategy(self):
        pass

        