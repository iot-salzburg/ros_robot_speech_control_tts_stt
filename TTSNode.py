#!/usr/bin/python
# An improvement would be that the robot only has to send the text and we analyze the language
# This would reduce the amount of work a robot programmer has to do
import os
import datetime

import rospy

from std_msgs.msg import String

def handle_output(data):
	if "espeak -v" in data.data:
		string = data.data
	else:
		string = "espeak -ven+m1 'An error occured. Please try again and or get in touch with your technician'"
	os.system(string)

def shutdown():
	"""This function is executed on node shutdown."""
	# command executed after Ctrl+C is pressed
	rospy.loginfo("Stopping Text-to-Speech Node")
	rospy.sleep(1)

def init():
	"""Initialize node and subscribe to necessary topics"""
    # initialize node
	rospy.init_node("tts_node")

    # Call custom function on node shutdown
	rospy.on_shutdown(shutdown)

	rospy.Subscriber("tts_node", String, handle_output)
	rospy.spin()

if __name__ == "__main__":
    init()
