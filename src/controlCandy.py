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

class controlCandy(object):
    def __init__(self):
        self.robot_name = 'mobile_base'
        self.spawn_candy_num = 0
        self.candy_list = []

        rospy.wait_for_service('/gazebo/spawn_urdf_model')
        self.spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        self.delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

        sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.callback)

        self.delete_th = 0.3

        self.start_flag = False

        self.start_time = 0

        #self.save_dir = './result/'

    def spawn_gazebo_models(self,name='candy',
                            model_type='ball',
                            model_pose=Pose(position=Point(x=0.6725, y=0.1265, z=0.7825)),
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
    
    def make_candy(self, num):   
        MIN_X = -2
        MAX_X = 2

        MIN_Y = -2
        MAX_Y = 2

        for candy_id in range(num): 
            _x = random.uniform(MIN_X,MAX_X)
            _y= random.uniform(MIN_Y,MAX_Y)
            spawn_candy_name = 'candy_' + str(candy_id)
            result = self.spawn_gazebo_models(name=spawn_candy_name, model_type='ball',model_pose=Pose(position=Point(x=_x, y=_y, z=1.0)))
            rospy.loginfo('success spawn candy: ' + str(candy_id))
            self.spawn_candy_num += 1
            self.candy_list.append(spawn_candy_name)
          
    def callback(self,data):
        names = data.name
        if self.robot_name in names:
            respRobot = self.get_model_state(self.robot_name,'')
            
            if respRobot.success:
                if not self.start_flag:
                    self.start_time = time.time()
                    self.start_flag = True
                    
                robot_pose = respRobot.pose
                for candy_num in range(self.spawn_candy_num):
                    
                    candy_id = 'candy_' + str(candy_num)
                    if candy_id in self.candy_list:
                        respCandy = self.get_model_state(candy_id,'')
                        
                        if respCandy.success:
                            distance = self.distance(robot_pose, respCandy.pose)
                            if distance < self.delete_th:
                                print("delete model")
                                self.delete_gazebo_models(candy_id)
                                self.candy_list.remove(candy_id)
                                self.delete_gazebo_models(candy_id)
                                if len(self.candy_list)==0:
                                    rospy.loginfo('All candy was Deleted COMPLETE!! time: ' + str(time.time() - self.start_time) )

            """        
            if len(self.candy_list) ==0:
                end_time = time.time() - self.start_time
                if not os.path.isdir(self.save_dir):
                    print('make dir: ' + self.save_dir)
                    os.makedirs(self.save_dir)
                f = open(self.save_dir + 'resulr.txt', 'w') # 書き込みモードで開く
                f.write(str(end_time)) # 引数の文字列をファイルに書き込む
                f.close()
            """
            
    def distance(self,p1,p2):
        diffX = p1.position.x - p2.position.x
        diffY = p1.position.y - p2.position.y
        
        d = math.sqrt(diffX*diffX + diffY*diffY)

        return d

    def delete_gazebo_models(self,name):
        try:
            delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
            resp_delete = delete_model(name)
            if resp_delete.success:
                rospy.loginfo('Delete:' + name)
            
        except rospy.ServiceException, e:
            rospy.loginfo('Delete Model service call failed: {0}'.format(e))

if __name__ == '__main__':
    rospy.init_node('check_candy')
    cc = controlCandy()
    cc.make_candy(5)

    rospy.spin()
    
