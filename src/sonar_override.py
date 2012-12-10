#!/usr/bin/env python

import roslib; roslib.load_manifest('sonar_override')
import rospy
import math
import sys

from std_msgs.msg import *
from geometry_msgs.msg import *

pub= rospy.Publisher('cmd_vel',Twist)

sonar_data = "0000"
joystick_data = None
multiplier = 1
def sonarCallback(data):
    global sonar_data
    sonar_data = data.data
    combinedCallback()

def joystickCallback(data):
    global joystick_data
    joystick_data = data
    combinedCallback()
    #pub.publish(joystick_data)

def gpsCallback(data):
    global multiplier = 1;
	if (data == 0) :
		multiplier= 0
	elif (data < 2):
		multiplier = 0.25
	elif (data < 5):
		multiplier = 0.5 
	elif (data <10) :
		multiplier = 1
	combinedCallback()

def combinedCallback():
    global joystick_data
    global sonar_data
    joystick_output = multiplier*joystick_data
    if ((sonar_data[0] == '1' or sonar_data[1] == '1') and joystick_data.linear.x > 0) or ((sonar_data[2] == '1' or sonar_data[3] == '1') and joystick_data.linear.x < 0):
        joystick_output.linear.x = 0
    pub.publish(joystick_output)

def main():
    rospy.init_node('sonarOverride', anonymous=False)
    rospy.Subscriber("sonar_step_detect", String, sonarCallback)
    rospy.Subscriber("joystick_cmd_vel", Twist, joystickCallback)
    rospy.Subscriber("GPSDistance", Float64, gpsCallback)
    rospy.spin()

if __name__ == '__main__':
    main()