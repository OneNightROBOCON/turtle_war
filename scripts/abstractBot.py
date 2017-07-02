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
        self.center_bumper = False
        self.left_bumper = False
        self.right_bumper = False
        #self.vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist,queue_size=1)
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist,queue_size=1)
        self.bumper_sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumperCallback)
        self.gazebo_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.gazeboCallback)

    def bumperCallback(self, data):
        if data.bumper == 0:
            if data.state == 1:
                self.left_bumper = True
            else:
                self.left_bumper = False
                
        if data.bumper == 1:
            if data.state == 1:
                self.center_bumper = True
            else:
                self.center_bumper = False

        if data.bumper == 2:
            if data.state == 1:
                self.right_bumper = True
            else:
                self.right_bumper = False
        
    def gazeboCallback(self, data):
        pass



    @abstractmethod
    def strategy(self):
        pass

