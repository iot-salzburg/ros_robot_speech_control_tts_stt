#!/usr/bin/python
# Wurde aus dem Sample Code von Pocketsphinx entnommen. Dies muss nur mehr umgeaendert werden, damit auch eine Deutsche Antwort erfolgen kann
# Optionen: problem, OK

import os
import datetime

import rospy

from std_msgs.msg import String

def handle_output(data):
   if "ok" is data:
      # String der die Sprachausgabe darstellt
      string = "espeak -vde+m1 'Roboter Sam konnte den Befehl erfolgreich exekutieren.'" 
      os.system(string)
   else:
      # String der die Sprachausgabe darstellt
      string = "espeak -vde+m1 'Roboter Sam konnte den Befehl NICHT erfolgreich exekutieren.'" 
      os.system(string)

def shutdown():
    """This function is executed on node shutdown."""
    # command executed after Ctrl+C is pressed
    rospy.loginfo("Stop ASRControl")
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
