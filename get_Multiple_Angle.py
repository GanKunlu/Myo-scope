'''
Created on 2016.5.21
edited on 2016.5.31
@Author: Gan
This program use to get 2 Myos' angle in real time.
the imported Myos_angle moudle has some functions that can caculate the angle from both ACC and GRY signals.

'''
import Myos_angle
from myo import init, Hub, Feed, StreamEmg
import time
import numpy as np
init()				# init the Myo
feed = Feed()	 	# use feed class
hub = Hub() 	
angle = [0,0]		# init 2 Myo's angle 
t_start = 0			# use to store the angle_updata function's start time
t_s = 0				# use to store the end time
T = 200				# Total time
t1 = 0				# to record the runing start time
t2 = 0				# to record current time
which_MYO = [0,1]	# choose which myo to use. threre are 4 types:[0],use the frist Myo; [1]:use the second; [0,1]or[1,0]:use both
hub.run(1000, feed)	
open('Angle&w.txt', 'w').close()
T = int(input("input time(s):"))

try:
	while True:
		myo = feed.get_devices()
		print(myo)
		t1 = time.time()
		GRY_start = time.time()
		time.sleep(1)
		t_start = time.time()
		
		angle = Myos_angle.angle_init(myo,angle,which_MYO)
		
		while hub.running:
			if myo:
				t_start = Myos_angle.get_angle(myo, angle, t_start, t_s, t1, t2, T, which_MYO)	
											
finally:
	hub.shutdown()  # !! crucial
	
