# turtle_war
turtle war !! ROS GAZEBO TURTLEBOT ROBOCON !!

## Quick Start
install turtlebot package
```
$ apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs
```

clone this repo
```
$ cd (YOUR-ROS-WORKSPACE)/src
$ clone https://github.com/dashimaki360/turtle_war.git
```

make
```
$ cd (YOUR-ROS-WORKSPACE)
$ catkin_make
```

launch (please open 3 terminals)
```
$ roslaunch turtle_war war_field.launch
$ roslaunch turtle_war minimal.launch
$ roslaunch turtle_war keyboard_teleop.launch
```

press 'i' GOGO turtlebot in gazebo~!!

maybe

## Env
- OS  : Ubuntu 14.04
- ROS : indigo
- GAZEBO : 2.


