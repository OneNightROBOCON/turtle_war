#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import rospy
import math
import rospkg
import copy
import random
import time
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import (
    Pose,
    Point,
)

from gazebo_msgs.srv import(
    SpawnModel,
    DeleteModel,
    GetModelState,
)

class Candy():
    def __init__(self, cdy_id, is_special):
        self.candy_id = cdy_id
        self.is_special = is_special
        self.name = 'candy_' + str(cdy_id)
        self.state = 0

class controlCandy(object):
    def __init__(self):
        self.DELETE_TH = 0.4  # m
        self.TIME_LIMIT = 120 #seconds
        self.SP_INTERVAL_TIME = 15
        self.robot_name = 'mobile_base'

        self.spawn_candy_num = 0
        self.candy_list = []
        self.robot_pose = Pose(position=Point(x=0., y=0., z=0.))

        rospy.wait_for_service('/gazebo/spawn_urdf_model')
        self.spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        self.delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

        sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.callback)

        self.start_flag = False
        self.end_flag = False
        self.sp_candy_flag = False
        self.start_time = 0
        self.last_sp_time = 0

        self.score = 0
        self.get_candy_num = 0
        self.get_sp_candy_num = 0

    def spawn_gazebo_models(self,name='candy',
                            model_type='ball',
                            model_pose=Pose(position=Point(x=0., y=0., z=0.5)),
                            model_reference_frame='world'):
        # Get Models' Path
        model_path = rospkg.RosPack().get_path('turtle_war')+'/models/'

        # Load model URDF
        model_xml = ''
        with open (model_path + model_type +'.urdf', 'r') as ball_file:
            model_xml=ball_file.read().replace('\n', '')

        # Spawn ball URDF
        resp_urdf = self.spawn_urdf(name, model_xml, '/', model_pose, model_reference_frame)


    def delete_gazebo_models(self,name='candy'):
        resp_delete = self.delete_model(name)
    
    def initCandy(self, num):
        for candy_id in range(num): 
            candy = Candy(candy_id, False)
            self.spawnCandy(candy)
            self.spawn_candy_num += 1
            candy.state = 5 # spawning
            self.candy_list.append(candy)

    def checkSpawnCandyPose(self, candy_pose):
        d = self.distance(self.robot_pose, candy_pose)
        return (d > 1.5) # m

    def spawnCandy(self, candy):
        MIN_X = -2
        MAX_X = 2

        MIN_Y = -2
        MAX_Y = 2

        is_candy_pose_ok = False
        while not is_candy_pose_ok:
            _x = random.uniform(MIN_X,MAX_X)
            _y= random.uniform(MIN_Y,MAX_Y)
            candy_pose = Pose(position=Point(x=_x, y=_y, z=0.5))
            is_candy_pose_ok = self.checkSpawnCandyPose(candy_pose)

        if self.sp_candy_flag:
            result = self.spawn_gazebo_models(name=candy.name, model_type='ball_sp',model_pose=candy_pose)
            #rospy.loginfo('success spawn SP candy: ' + str(candy.candy_id))
            candy.is_special = True
            self.last_sp_time = time.time()
            self.sp_candy_flag = False
        else:
            result = self.spawn_gazebo_models(name=candy.name, model_type='ball',model_pose=candy_pose)
            candy.is_special = False
            #rospy.loginfo('success spawn candy: ' + str(candy.candy_id))


    def callback(self,data):
        if self.end_flag:
            return
        if self.start_flag:
            # main part
            robot_idx = data.name.index(self.robot_name)
            robot_pose = data.pose[robot_idx]
            for candy in self.candy_list:
                if candy.state == 1: # exist
                    if not candy.name in data.name:
                        candy.state = 4
                        continue
                    candy_idx = data.name.index(candy.name)
                    candy_pose = data.pose[candy_idx]
                    distance = self.distance(robot_pose, candy_pose)
                    if distance < self.DELETE_TH:
                        candy.state = 2 #to_delete
                        if candy.is_special:
                            self.score += 5
                            self.get_sp_candy_num += 1
                        else:
                            self.score += 1
                            self.get_candy_num += 1
                elif candy.state ==2: # to_delete
                    pass
                elif candy.state ==3: # deleting
                    if not candy.name in data.name:
                        candy.state = 4 # to_spawn
                elif candy.state ==4: # to_spawn
                    pass
                elif candy.state ==5: # spawning
                    if candy.name in data.name:
                        candy.state = 1 # exist
                elif candy.state ==0: # init
                    pass
        # check robot spawn
        else:
            if self.robot_name in data.name:
                respRobot = self.get_model_state(self.robot_name,'')
                if respRobot.success:
                    if not self.start_flag:
                        self.start_time = time.time()
                        self.last_sp_time = time.time()
                        self.start_flag = True

    def distance(self,p1,p2):
        diffX = p1.position.x - p2.position.x
        diffY = p1.position.y - p2.position.y
        d = math.sqrt(diffX*diffX + diffY*diffY)
        return d

    def delete_gazebo_models(self,name):
        try:
            delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
            resp_delete = delete_model(name)
            #if resp_delete.success:
                #rospy.loginfo('Delete:' + name)
        except rospy.ServiceException, e:
            rospy.loginfo('Delete Model service call failed: {0}'.format(e))

    def deleteAndTheSpawn(self):
        if self.start_flag == True and self.end_flag == False:
            for candy in self.candy_list:
                if candy.state == 1: # exist
                    pass
                elif candy.state ==2: # to_delete
                    self.delete_gazebo_models(candy.name)
                    candy.state = 3
                elif candy.state ==3: # deleting
                    pass
                elif candy.state ==4: # to_spawn
                    self.spawnCandy(candy)
                    candy.state = 5
                elif candy.state ==5: # spawning
                    pass
                elif candy.state ==0: # init
                    pass

    def chekeSpCandyTime(self):
        if self.start_flag == True and self.end_flag == False and self.sp_candy_flag == False:
            if (time.time() - self.last_sp_time) > self.SP_INTERVAL_TIME:
                self.sp_candy_flag = True
                rospy.loginfo('NEXT CANDY IS SPECIAL!!' )

    def chekeTimeup(self):
        if self.start_flag == True and self.end_flag == False:
            passed_time = time.time() - self.start_time
            if  passed_time > self.TIME_LIMIT:
                rospy.loginfo('!!!!!!!!!!!!! Time is Up !!!!!!!!!!!!!' )
                rospy.loginfo('  SCOREx : ' + str(self.score) )
                rospy.loginfo('  Candyx : ' + str(self.get_candy_num) )
                rospy.loginfo('SP Candy : ' + str(self.get_sp_candy_num) )
                rospy.loginfo('!!!!!!!!!!!!!     end    !!!!!!!!!!!!!' )
                self.end_flag = True

if __name__ == '__main__':
    rospy.init_node('check_candy')
    cc = controlCandy()
    cc.initCandy(20)

    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        cc.deleteAndTheSpawn()
        cc.chekeSpCandyTime()
        cc.chekeTimeup()
        r.sleep()

