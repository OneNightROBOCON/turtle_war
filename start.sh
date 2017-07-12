gnome-terminal -e "/opt/ros/indigo/bin/roslaunch turtle_war make_field.launch"

sleep 5

gnome-terminal -e "/opt/ros/indigo/bin/roslaunch turtle_war spawn_robot.launch"
