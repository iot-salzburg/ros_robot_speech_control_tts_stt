#!/usr/bin/env python
# This is the Speech to Text Node
# Newest Version!!!

import os
import sys
import time
import rospy
import speech_recognition as sr
from termios import tcflush, TCIFLUSH
from std_msgs.msg import String
from snips_nlu import SnipsNLUEngine
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import wave
import numpy as np
from joblib import load
import pyaudio


def getCommand(sentence, language):
# The variable "name", "intent" and "slot" needs to be extracted:
    # Default values due to runtime thingies -> Exception etc
	intent = "None"
	name = "None"
	variable = "None"

    # The language Model gets loaden
	# For additonal languages please alter/change here
	if language == "de":
    		nlu_engine = SnipsNLUEngine.from_path("SnipsNLU/RobotControlDeutsch_TrainedModel")
	else:
		nlu_engine = SnipsNLUEngine.from_path("SnipsNLU/RobotControlEnglish_TrainedModel")

	parsing = nlu_engine.parse(sentence)
	intent = parsing["intent"]["intentName"]
	
	# Explaination, because otherwise I would forget why I did, what I did...
	# parsing is a dictionary
	# parsing["slots"] is a list
	# x is a dictionary, as well as the rest...
	for x in parsing["slots"]:
		if x["slotName"] == "robo_name":
			name = x["value"]["value"]

	if intent.encode('utf-8') != "PO".encode('utf-8'):
		# Explaination, because otherwise I would forget why I did, what I did...
		# parsing is a dictionary
		# parsing["slots"] is a list
		# x is a dictionary, as well as the rest...
		for x in parsing["slots"]:
			if x["slotName"] == "storage_slot":
				variable = x["value"]["value"]
	
	return intent, name, variable;

def sentToTTS(pub_tts, string, rate):
    # Sends the string to the TTS Node Topic
	pub_tts.publish(string)
	rate.sleep()
	#os.system(string)

def publishCommand(pub_stt, msg, rate):
	pub_stt.publish(msg)
	rate.sleep()

    # Die folgenden Zeilen bleiben noch zur Sicherheit im Code
    # string = "rostopic pub_stt /stt_node pocketsphinx/OutputNode '{name: Sam, sprache: de, nachricht: Fach 9}'"
    # os.system(string)
    # os.system("ctrl-C")
	
def checkRobo(robo_name, intent):
	# For a more dynamic and advanced system the ros core could be used to find the robots and the functions/topics they have.

	if robo_name == "Sam" or robo_name == "Husky":
		robo_available = True	
		if intent == "None":
			intent_available = False
			available = False
		else:
			intent_available = True
			available = True
		
	else:
		available = False
		robo_available = False
		intent_available = False
		
	return available, robo_available, intent_available
	
def RoboFeedback(robo_available, intent_available, language):
	# The differentiation between the two languages could be (vastly) improved. Probably a point for future work
	if not robo_available and not intent_available:
		if language == "en":
			string = "espeak -ven+m1 'The robot and task are NOT available'"
		else:
			string = "espeak -vde+m1 'Der Roboter und Funktion sind NICHT verfuegbar'"
					
	elif not robo_available:
		if language == "en":
			string = "espeak -ven+m1 'The robot is NOT available'"
		else:
			string = "espeak -vde+m1 'Der Roboter ist NICHT verfuegbar'"
						
	elif not intent_available:
		if language == "en":
			string = "espeak -ven+m1 'The function for the intent is not available'"
		else:
			string = "espeak -vde+m1 'Die Funktion des Kommandos ist nicht verfuegbar'"
						
	else:
		if language == "en":
			string = "espeak -ven+m1 'Something went terribly wrong. Unfortunately not sure what it is...'"
		else:
			string = "espeak -vde+m1 'Etwas lief schief. Leider ist nicht bekannt was es ist...'"

	return string

def getLID(sig):
	(rate, sig) = wav.read('command.wav')
	mfcc_feat = mfcc(sig, rate, numcep=26) #mfcc_feat -> numpy.ndarray
	mfcc_feat = mfcc_feat.sum(axis=0)
	model = load('LID/saved_SVM_Model.joblib')
	x = np.reshape(mfcc_feat, (1, -1))
	predict = model.predict(x)
	if np.array_equal(predict, np.array([0.0])):
		return 'en'
	else:
		return 'de'
	
def saveAudio(audio):
	with open('command.wav', 'wb') as f:
		f.write(audio.get_wav_data())


def speakSTT(pub_stt, pub_tts):
	r = sr.Recognizer()
        rate = rospy.Rate(10)

	while True:
		# For the standard output text we could define a default language
	    string = "espeak -ven+m1 'To record a speech command please push the button r'" 
	    sentToTTS(pub_tts, string, rate)
            a = raw_input("To record please push the button r\n Fuer eine Sprachaufnahme bitte r drucken\n")
	    if a == "r":
			with sr.Microphone() as source:
				# Muss auch an die TTS-Node uebergeben werden
				print("Talk to me!")
				print("Sprich zu mir!")
				string = "espeak -vde+m1 'Talk to me!'" 
				sentToTTS(pub_tts, string, rate)
				time.sleep(2)
				audio = r.listen(source)
				tcflush(sys.stdin, TCIFLUSH)
	    else:
			pass
			
	    try:              			
			saveAudio(audio)			
			language='de' #en
			# Hier muss noch die Spracherkennung eingearbeitet werden...	
			language = getLID(audio)
			sentence = r.recognize_google(audio, language=language)

			# The differentiation between the two languages could be (vastly) improved. Probably a point for future work
			if language == "de":
				string = "Du hast gesagt: " + sentence
				string = "espeak -vde+m1 '" + string + "'"
				print(string)
				sentToTTS(pub_tts, string, rate)
				
			if language == "en":
				string = "You said: " + sentence
				string = "espeak -ven+m1 '" + string + "'"
				print(string)
				sentToTTS(pub_tts, string, rate)	

			# A function that analyzes the sentence and outputs the robo_name, intent and variables/slots
			intent, robo_name, variable = getCommand(sentence, language)
			
			# Check if robots are available
			available, robo_available, intent_available = checkRobo(robo_name, intent)
			if(available):
				msg = intent + " " + variable
				
				if language == "en":
					string = "espeak -ven+m1 'The robot and task are available'"
					sentToTTS(string, pub_stt)                
				
				else:
					string = "espeak -vde+m1 'Der Roboter und Funktion sind verfuegbar'"
					sentToTTS(pub_tts, string, rate)
				
				# publish the command to the topic
				publishCommand(pub_stt, msg, rate)
			
			else:
				string = RoboFeedback(robo_available, intent_available, language)
				sentToTTS(pub_tts, string, rate)
						
	    except sr.UnknownValueError:
			# Dieser String muss auch noch zu dem TTS-Node Transportiert werden		
			print("Something went wrong with the transformation. Please try again")
	    except sr.RequestError as e:
			# Dieser String muss auch noch zu dem TTS-Node Transportiert werden
			print("Google Speech Recognition did not give back the transformed string; {0}".format(e))

def shutdown():
    """This function is executed on node shutdown."""
    # command executed after Ctrl+C is pressed
    rospy.loginfo("Stopping STT Node")
    rospy.sleep(1)

def init():
	"""Initialize node and subscribe to necessary topics"""

	# initialize node
	rospy.init_node("stt_node")
	pub_stt = rospy.Publisher('stt_node', String)
	pub_tts = rospy.Publisher('tts_node', String)

	# Call custom function on node shutdown
	rospy.on_shutdown(shutdown)

	speakSTT(pub_stt, pub_tts)

if __name__ == "__main__":
	init()
