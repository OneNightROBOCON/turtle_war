#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from gazebo_msgs.msg import ModelStates 
import rospy

class AbstractBot(object):
    __metaclass__ = ABCMeta

    def __init__(self, bot_name):
        self.name = bot_name
        self.bumper = BumperEvent()
        self.vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist,queue_size=1)
        self.bumper_sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumperCallback)
        self.gazebo_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.gazeboCallback)

    def bumperCallback(self, data):
        if self.bumper.state == 0:
            self.bumper = data

    def gazeboCallback(self, data):
        pass

    @abstractmethod
    def strategy(self):
        pass

