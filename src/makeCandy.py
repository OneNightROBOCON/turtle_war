#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random
import time

from gazebo_msgs.srv import (
    SpawnModel,
    DeleteModel,
)
from geometry_msgs.msg import (
    Pose,
    Point,
)


def spawn_gazebo_models(name="candy", 
                        model_type="ball",
                        model_pose=Pose(position=Point(x=0.6725, y=0.1265, z=0.7825)),
                        model_reference_frame="world"):
    # Get Models' Path
    model_path = rospkg.RosPack().get_path('turtle_war')+"/models/"

    # Load model URDF
    model_xml = ''
    with open (model_path + model_type +".urdf", "r") as ball_file:
        model_xml=ball_file.read().replace('\n', '')

    # Spawn ball URDF
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf(name, model_xml, "/",
                               model_pose, model_reference_frame)
        return True

    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))
        return False

def delete_gazebo_models(name="candy"):
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model(name)
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

def update(object_dict):
    
    DELETE_TIME = 5 

    current_time = time.time()
    for key in list(object_dict.keys()):
        if current_time - object_dict[key] > DELETE_TIME:
            delete_gazebo_models(key)
            del object_dict[key]

def all_delete(object_dict):
    for key in list(object_dict.keys()):
        delete_gazebo_models(key)
        del object_dict[key]


def make_candy():
    r = rospy.Rate(0.25) # sampling time

    MIN_X = -1
    MAX_X = 1

    MIN_Y = -1
    MAX_Y = 1

    current_candy_num = 0
    candy_id = 0
    candy_dict ={}
    start_time = time.time()
    while time.time() - start_time < 20: 
        _x = random.uniform(MIN_X,MAX_X)
        _y= random.uniform(MIN_Y,MAX_Y)
        spawn_candy_name = "candy_" + str(candy_id)
        result = spawn_gazebo_models(name=spawn_candy_name, model_type="ball",model_pose=Pose(position=Point(x=_x, y=_y)))
        if result:
            t = time.time()
            candy_dict[spawn_candy_name] = t
            candy_id +=1

        update(candy_dict)

        r.sleep()
    
    all_delete(candy_dict)


if __name__ == '__main__':
    rospy.init_node("make_candy_node")
    
    make_candy() 	
    
    

