#!/usr/bin/env python
# Old Version!!!

import os
import sys
import time
import rospy
import speech_recognition as sr
from termios import tcflush, TCIFLUSH
from std_msgs.msg import String

def getCommand(sentence):
    
    if "drucker" in sentence.lower() and "ausgabe" in sentence.lower():
        name = "PO"
        nachricht = "keine Nachricht"

    elif "drucker" in sentence.lower() and "lager" in sentence.lower():
        name = "PS"
        if "1" in sentence.lower() or "eins" in sentence.lower():
            nachricht = "1"
        if "2" in sentence.lower() or "zwei" in sentence.lower():
            nachricht = "2"
        if "3" in sentence.lower() or "drei" in sentence.lower():
            nachricht = "3"
        if "4" in sentence.lower() or "vier" in sentence.lower():
            nachricht = "4"
        if "5" in sentence.lower() or "fuenf" in sentence.lower():
            nachricht = "5"
        if "6" in sentence.lower() or "sechs" in sentence.lower():
            nachricht = "6"
        if "7" in sentence.lower() or "sieben" in sentence.lower():
            nachricht = "7"
        if "8" in sentence.lower() or "acht" in sentence.lower():
            nachricht = "8"
        if "9" in sentence.lower() or "neun" in sentence.lower():
            nachricht = "9"
        else:
            nachricht = "keine Nachricht"

    elif "lager" in sentence.lower() and "ausgabe" in sentence.lower():
        name = "SO"
        if "1" in sentence.lower() or "eins" in sentence.lower():
            nachricht = "1"
        if "2" in sentence.lower() or "zwei" in sentence.lower():
            nachricht = "2"
        if "3" in sentence.lower() or "drei" in sentence.lower():
            nachricht = "3"
        if "4" in sentence.lower() or "vier" in sentence.lower():
            nachricht = "4"
        if "5" in sentence.lower() or "fuenf" in sentence.lower():
            nachricht = "5"
        if "6" in sentence.lower() or "sechs" in sentence.lower():
            nachricht = "6"
        if "7" in sentence.lower() or "sieben" in sentence.lower():
            nachricht = "7"
        if "8" in sentence.lower() or "acht" in sentence.lower():
            nachricht = "8"
        if "9" in sentence.lower() or "neun" in sentence.lower():
            nachricht = "9"
        else:
            nachricht = "keine Nachricht"

    else:
        name = "kein Name"
        nachricht = "keine Nachricht"

    # Der Lagerplatz wird extrahiert, da dieser momentan nur sehr gering von dem RegEx erkannt wird... nur zur Sicherheit
    nachricht = [int(s) for s in sentence.split() if s.isdigit()]
    nachricht = str(nachricht[0])

    return name, nachricht;

def sentToTTS(string):
    os.system(string)

def publishCommand(pub, msg, rate):
    pub.publish(msg)
    rate.sleep()

    # Die folgenden Zeilen bleiben noch zur Sicherheit im Code
    # string = "rostopic pub /stt_node pocketsphinx/OutputNode '{name: Sam, sprache: de, nachricht: Fach 9}'"
    # os.system(string)
    # os.system("ctrl-C")

def speakSTT(pub):

	r = sr.Recognizer()
        rate = rospy.Rate(10)

	while True:
	    string = "espeak -vde+m1 'Um Aufzunehmen bitte r druecken'" 
	    sentToTTS(string)
            a = raw_input("Um Aufzunehmen bitte r druecken\n")
	    if a == "r":
		with sr.Microphone() as source:
		    # Muss auch an die TTS-Node uebergeben werden
		    print("Sprich zu mir!")
		    string = "espeak -vde+m1 'Sprich zu mir!'" 
		    sentToTTS(string)
		    time.sleep(2)
		    audio = r.listen(source)
		    tcflush(sys.stdin, TCIFLUSH)
	    else:
		pass
	    try:              
		# Hier muss noch die Spracherkennung eingearbeitet werden...		
		sentence = r.recognize_google(audio, language="de") #en

		string = "Google Speech Recognition glaubt du sagst: " + sentence
		print(string)
                sentToTTS(string)

                # Hier jetzt ne Funktion die Analysiert, was in dem Befehl steht und ob es ausfuehrbar ist...
                name, nachricht = getCommand(sentence)
                msg = name + " " + nachricht

                # A function that takes care of the language output
                # sendToTTS()                

                # Publish the command to the topic
                publishCommand(pub, msg, rate)

	    except sr.UnknownValueError:
		# Dieser String muss auch noch zu dem TTS-Node Transportiert werden		
		print("Google Speech Recognition konnte dich leider nicht verstehen")
	    except sr.RequestError as e:
		# Dieser String muss auch noch zu dem TTS-Node Transportiert werden
		print("Konnte kein Ergebniss von Google Speech Recognition erhalten; {0}".format(e))

def shutdown():
    """This function is executed on node shutdown."""
    # command executed after Ctrl+C is pressed
    rospy.loginfo("STT Node wird angehalten")
    rospy.sleep(1)

def init():
    """Initialize node and subscribe to necessary topics"""

    # initialize node
    rospy.init_node("stt_node")
    pub = rospy.Publisher('stt_node', String)

    # Call custom function on node shutdown
    rospy.on_shutdown(shutdown)

    speakSTT(pub)

if __name__ == "__main__":
    init()
