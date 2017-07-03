#include "ros/ros.h"
#include <termios.h>
#include <stdio.h>
#include <signal.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>

#define MAV 3.14
#define MLV 2.0

#define RIGHT 0x43
#define LEFT 0x44
#define FORWARD 0x41
#define BACK 0x42
#define STOP 0x20


class RoboCtrl
{
	public:
		RoboCtrl()
		{
			ros::NodeHandle node;
			odom_sub_ = node.subscribe("odom", 1, &RoboCtrl::odomCallback, this);
			twist_pub_ = node.advertise<geometry_msgs::Twist>("cmd_vel", 1);


		}
		void moveRobo()
		{
			geometry_msgs::Twist twist;
			char c;
			int kfd = 0;
			struct termios cooked,raw;
			tcgetattr(kfd, &cooked);
			memcpy(&raw,&cooked,sizeof(struct termios));
			raw.c_lflag &=~(ICANON|ECHO);
			raw.c_cc[VEOL] = 1;
			raw.c_cc[VEOF] = 2;
			tcsetattr(kfd, TCSANOW, &raw);
			if(read(kfd, &c, 1)<0)
			{
				exit(-1);
			}
			twist.linear.x = 0;
			twist.angular.z = 0;
			switch(c)
			{
				case LEFT:
					twist.angular.z = MAV;
					break;
				case RIGHT:
					twist.angular.z = -MAV;
					break;
				case FORWARD:
					twist.linear.x = MLV;
					break;
				case BACK:
					twist.linear.x = -MLV;
					break;
				case STOP:
					twist.linear.x = 0;
					twist.angular.z = 0;
					break;
				default:
					break;
			}
			twist_pub_.publish(twist);
		}
		void odomCallback(const nav_msgs::Odometry &odom)
		{
			return;
		}
			

	private:
		ros::Subscriber odom_sub_;
		ros::Publisher twist_pub_;
};

int main(int argc, char **argv)
{
	ros::init(argc, argv, "robo_ctrl");
	RoboCtrl robo_ctrl;
	ros::Rate r(100);
	while (ros::ok())
	{
		robo_ctrl.moveRobo();
		ros::spinOnce();
		r.sleep();
	}
}
