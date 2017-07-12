#!/bin/sh
echo "turtlebot install"
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs -y

echo "python OppenCV setting"
sudo apt-get install python-numpy -y
sudo apt-get install python-opencv -y

echo "Get turtle_war"
sudo apt-get install git -y
cd ~/catkin_ws/src
git clone https://github.com/OneNightROBOCON/turtle_war

echo "catkin make"
cd ~/catkin_ws
catkin_make

echo "run turtle_war"
roscd turtle_war
chmod 777 start.sh
bash start.sh
