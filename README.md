# README.md

Die zwei wichtigsten Folder sind MultilingualROSSpeechControl sowie ros_robot_speech_control (niks_experiments) . In Multilingual... befinden sich die zwei Programme STTNode.py und TTSNode.py. Im niks_experiments Ordner (unter src) StretchingSpeech.cpp. Es befinden sich hier noch mehrere andere Files, was daran liegt, dass dies nur eine Kopie von niks_experiments ist.

### Befehle:

### Das Paket nikes_experiments ist hier auf git unter ros_robot_speech_control
 zu finden:
 
roslaunch franka_control franka_control.launch robot_ip:=192.168.13.1
roslaunch panda_moveit_config panda_moveit.launch
roslaunch panda_moveit_config moveit_rviz.launch


source workspace/devel/setup.bash
rosrun niks_experiments StretchingSpeech


### Das Paket MultilingualROSSpeechControl ist hier auf git unter ros_robot_speech_control_tts_stt
zu finden:

cd workspace/src/MultilingualROSSpeechControl/
python TTSNode.py

cd workspace/src/MultilingualROSSpeechControl/
python STTNode.py


### Sonstiges

franka::RealtimeConfig::kIgnore must be set when instantiating franka::Robot class.

Otherwise the robot just runs with an FULL_PREEMPT_RT Kernel. Means: No Nvidia Drivers.

This hast to be edited inside franka_ros/franka_control/franka_control_node.cpp. 

