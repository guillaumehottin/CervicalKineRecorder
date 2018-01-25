import matplotlib.pyplot as plt
import numpy as np
import os
import math
from functools import reduce


#################################################
#Get data in name_dir/name_file
def get_file_data(name_file,name_dir):
	f = open(name_dir+'/'+name_file,"r")
	data = f.readlines()
	yaw_l, pitch_l, roll_l = [],[],[]
	data.pop(0)

	#Ignore data with not enough points
	if (len(data)>900):
		for i in range(0,len(data)):
			elems = data[i].split(" ")
			yaw_l.append(elems[0])
			pitch_l.append(elems[1])
			roll_l.append(elems[2])
	#Convert to float
	if (yaw_l != []):
		yaw_l = list(map(float, yaw_l))
		pitch_l = list(map(float, pitch_l))
		roll_l = list(map(float, roll_l))

	return yaw_l,pitch_l,roll_l





#################################################
#Save or plot curves with data in name_dir/name_file
def save_or_plot_figs(name_file,name_dir,save,plot):
	#get data
	yaw_l,pitch_l,roll_l = get_file_data(name_file,name_dir)
	# row and column sharing
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
	ax1.plot(yaw_l, pitch_l)
	ax1.set_title('pitch = f(yaw)')
	ax2.plot(pitch_l, roll_l)
	ax2.set_title('roll= f(pitch)')
	ax3.plot(roll_l, yaw_l, color='r')
	ax3.set_title('yaw= f(roll)')
	ax4.plot([], [])

	if save:
		new_name = (name_dir+'/'+name_file).split(".")[1]
		plt.savefig('.'+new_name+".png")
		plt.close(fig)
	if plot:
		plt.show()
	
#################################################
#Save or plot call curves for one motion
def save_or_plot_all(motion,name_dir,save,plot):
	stg = motion + ".orpl"
	list_dir = os.listdir(name_dir)
	l = []

	for name in list_dir:
		if stg in name:
			l += [name]
	for name in l:
		if save:
			save_or_plot_figs(name,name_dir,save,plot)
		if plot:
			save_or_plot_figs(name,name_dir,save,plot)





#################################################
# motion_type : "Roulis", "Lacet" or "Tangage"
# name_user   : name of the folder which contains user data 
# Return      : all data for a specific user with the correct motion
# Example     : yaw =[all_yaw_at_date_1, all_yaw_at_date_2, ....]
#################################################

def get_patient_data_motion(name_folder,motion_type):
	#select all files with the correct motion
	stg = motion_type+".orpl"
	#Get names of all files in name_user
	list_dir = os.listdir(name_folder)
	list_files = []

	#Keep names like *stg
	for name in list_dir:
		if stg in name:
			list_files += [name]
	#Get all data
	yaw,pitch,roll = [],[],[]
	for name_file in list_files:
		#Get data
		yaw_l,pitch_l,roll_l = get_file_data(name_file,name_folder)

		#Add to result
		yaw.append(yaw_l)
		pitch.append(pitch_l)
		roll.append(roll_l)

	return yaw,pitch,roll



#################################################
#Get data of all patients
def get_all_data_motion(motion):
	#Get names of all folders
	list_dir = [x[0] for x in os.walk('.')]
	list_dir.pop(0)
	print(list_dir)
	all_yaw,all_pitch,all_roll = [],[],[]

	for directory in list_dir:
		#Get data of a specific user and motion
		yam,pitch,roll = get_patient_data_motion(directory,motion)
		#Append to result
		all_yaw.append(yaw)
		all_pitch.append(pitch)
		all_roll.append(roll)

	return all_yaw,all_pitch,all_roll




###############################################################################

def get_classical_file_data(name_dir,motion):
	#Find classical measures
	print(name_dir+'/commentaires.txt')
	f = open(name_dir+'/commentaires.txt',"r")
	data_com = f.readlines()
	list_files = []
	for i in range(0,len(data_com)):

		file_split = data_com[i].split(":")
		if (file_split[1] == ' \n' and motion in file_split[0]):
			name = file_split[0]+'.orpl'
			list_files.append(name.replace(' .orpl','.orpl'))
	print(list_files)
	f.close()
	#Get data
	yaw,pitch,roll = [],[],[]
	for name_file in list_files:
		f = open(name_dir+'/'+name_file,"r")
		data = f.readlines()
		yaw_l, pitch_l, roll_l = [],[],[]
		data.pop(0)

		for i in range(0,len(data)):
			elems = data[i].split(" ")
			yaw_l.append(elems[0])
			pitch_l.append(elems[1])
			roll_l.append(elems[2])
		#Convert to float
		if (yaw_l != []):
			yaw_l = list(map(float, yaw_l))
			pitch_l = list(map(float, pitch_l))
			roll_l = list(map(float, roll_l))
		f.close()
		yaw.append(yaw_l)
		pitch.append(pitch)
		roll.append(roll)

	return yaw,pitch,roll

####################################################################"
def convex_hull_graham(points):
    '''
    Returns points on convex hull in CCW order according to Graham's scan algorithm. 
    By Tom Switzer <thomas.switzer@gmail.com>.
    '''
    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

    def cmp(a, b):
        return (a > b) - (a < b)

    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def _keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


#angle_1 : List of float ( for instance, yam = [0.,0.001,.....] )
#angle_2 : Same
#Plot    : Bool ( If TRUE : Plot curve with convex hull and extreme points )
def convex_hull(angle_1,angle_2,plot):
	l_hull = []
	for i in range(0,len(y)):
		l_hull.append([angle_1[i],angle_2[i]])	
	hull = convex_hull_graham(l_hull)
	angle_1_hull,angle_2_hull = [],[]
	for j in range(0,len(hull)):
		angle_1_hull.append(hull[j][0])
		angle_2_hull.append(hull[j][1])
	#Find extreme
	x_min = np.min(angle_1_hull)
	x_max = np.max(angle_1_hull)
	y_min = np.min(angle_2_hull)
	y_max = np.max(angle_2_hull)
	border_l = [x_min,x_max,y_min,y_max]
	if (plot):
		plt.plot(y,p,'b')
		plt.plot(angle_1_hull,angle_2_hull,'r--')
		plt.axhline(y_min,color='g', linestyle='--')
		plt.axhline(y_max,color='g', linestyle='--')
		plt.axvline(x_min,color='g', linestyle='--')
		plt.axvline(x_max,color='g', linestyle='--')
		plt.show()
	return hull, bordel_l	

###############################################################################
#Main
"""
motions = ['Roulis','Lacet']
list_dir = [x[0] for x in os.walk('.')]
list_dir.pop(0)
print(list_dir)
for directory in list_dir:
	for motion in motions:
		save_or_plot_all(motion,directory,True,False)
"""
"""
yaw,pitch,roll = get_patient_data_motion("abad_charlene_21","Lacet")
#print len([yaw,pitch,roll])
l = compute_mean_patient(yaw,pitch,roll)
print(l)
"""


y,p,r = get_file_data("Wed Dec  6 10_56_17 2017 - Lacet.orpl","abad_charlene_21")
hull, border_l = convex_hull(y,p,True)
