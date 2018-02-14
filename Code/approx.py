import matplotlib.pyplot as plt
import numpy as np
import os
import math
import numpy as np
from scipy.misc import comb
from scipy import interpolate
import pylab as plb
from plot_save import normalize
import glob
import sklearn.decomposition as skd
import random

global cpt ,l

def get_file_data(path):
	f = open(path,"r")
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

	return yaw_l,pitch_l,roll_l


########################################################
#Compute distance between two consecutives points
#for the main axis of motion
#For yaw motion -> Main axis = yaw
#For pitch motion -> Main axis = Pitch
########################################################
def compute_difference_list_motion(angle_x,angle_y,id_curve):
	if(id_curve==1 or id_curve==3):  #Lacet or Roulis
		#Detect two ways
		diff_l = [angle_x[i]-angle_x[i+1] for i in range(len(angle_x)-1)]
			
	elif(id_curve==2):#Tangage
		diff_l = [angle_y[i]-angle_y[i+1] for i in range(len(angle_y)-1)]
	else:		  
		diff_l = []
	return diff_l


######################################################
#Remove parasite motion
#At the end of one way motion for instance
######################################################
def remove_parasite_motion(angle_x,angle_y,id_curve,threshold=0.1):

	diff_l = compute_difference_list_motion(angle_x,angle_y,id_curve)
	index_to_remove = []
	for i in range(len(diff_l)):
		if(np.abs(diff_l[i])<threshold):
			index_to_remove.append(i+1)

	#update angle_x and angle_y
	n = len(list(angle_x))
	angle_x = [angle_x[ind] for ind in range(n) if ind not in index_to_remove]
	angle_y = [angle_y[ind] for ind in range(n) if ind not in index_to_remove]
	#Recompute diff_l
	diff_l = compute_difference_list_motion(angle_x,angle_y,id_curve)
	return angle_x,angle_y,diff_l

########################################################
# Detect each two ways
# Input:
#	 _ diff : List
# Output:
#	 _ List with index for all two ways beginning
########################################################


def detect_two_ways(diff_l):
	sign_l = np.sign(diff_l)
	index_change_l = [0]
	sign = sign_l[0]
	for i in range(len(sign_l)):
		if(sign_l[i]!=sign and sign_l[i]!=0):
			index_change_l.append(i)
			sign = sign_l[i]
	index_change_l = index_change_l[::2]
	return index_change_l

########################################################
#Have same number of points for each two ways and compute mean
#Inputs:
#	_ two_ways_x : List of List with each two ways for axis x
#	_ two_ways_y : Same with axis y
########################################################
def mean_control_points(two_ways_x,two_ways_y):
	#Get same number of points of each two ways
	min_len = min(map(len, two_ways_x))
	for i in range(len(two_ways_x)):
		n = len(two_ways_x[i])
		two_ways_x[i] = [two_ways_x[i][j + j*(n-min_len)/min_len] for j in range(min_len)]
		two_ways_y[i] = [two_ways_y[i][j + j*(n-min_len)/min_len] for j in range(min_len)]
	mean_control_x = [float(sum(col))/len(col) for col in zip(*two_ways_x)]
	mean_control_y = [float(sum(col))/len(col) for col in zip(*two_ways_y)]
	return mean_control_x,mean_control_y


########################################################
# Compute mean control points for two ways
# Detect each two ways, get same number of points
# and mean each list
# Inputs:
#	 _ angle_x : List
#	 _ angle_y : List
#	 _ id_curve: int
#Outputs:
#	 _ Control points
########################################################
def get_control_points(angle_x,angle_y,id_curve):

	#Remove very small motions
	angle_x,angle_y,diff_l = remove_parasite_motion(angle_x,angle_y,id_curve,threshold=0.1)	

	#Two ways
	index_change_l = detect_two_ways(diff_l)	
	#Build list for each two ways
	two_ways_x, two_ways_y = [],[]
	for i in range(len(index_change_l)-1):
		two_ways_x += [angle_x[index_change_l[i]:index_change_l[i+1]]]
		two_ways_y += [angle_y[index_change_l[i]:index_change_l[i+1]]]
		
	two_ways_x += [angle_x[index_change_l[-1]:]]
	two_ways_y += [angle_y[index_change_l[-1]:]]

	#Mean
	mean_control_x,mean_control_y = mean_control_points(two_ways_x,two_ways_y)
	
	print "Mean"
	print mean_control_x
	return mean_control_x,mean_control_y


########################################################
# Compute final control points
# And Interpolate data
# Inputs:
#	 _ angle_x : List
#	 _ angle_y : List
#	 _ id_curve: int
#Outputs:
#	 _ Spline curve
########################################################
def interpolate_spline(angle_x,angle_y,id_curve,nb_points=500):
	global l
	#1) Choose control points
	x_control,y_control = get_control_points(angle_x,angle_y,id_curve)
	l = [x_control,y_control]
	#2)Interpolate
	#Inputs  :
	#	s: smoothing condition
	#Outputs : 
	#	tck : tuple (t,c,k) vector of knots, B-spline coeff and the degree
	#	u   : weighted sum of squared residuals of the approximation
	tck,u=interpolate.splprep([x_control,y_control],s=0.0)
	x_spline,y_spline= interpolate.splev(np.linspace(0,1,nb_points),tck)

	return x_spline,y_spline


########################################################
# Get data in list_path and normalize it
# Inputs:
#	 _ list_path: List
#	 _ id_curve: int
#Outputs:
#	 _ List of List with all angles
#	 _ list_name : List with names of all patients
########################################################	
def adapt_all_curves(list_path,id_curve):
	yaw_l,pitch_l,roll_l = [],[],[]
	list_name = []
	list_sym = []
	
	for path in list_path:	
		#Get data and normalize it
		yaw,pitch,roll  = get_file_data(path)
		yaw,pitch,roll  = normalize(yaw,pitch,roll)

		yaw_l.append(yaw)
		pitch_l.append(pitch)
		roll_l.append(roll)
		list_name.append(path.split('/')[1])

	return yaw_l,pitch_l,roll_l,list_name

#################################################################################
## Script plots
def plot_example(list_path,id_curve):
	global cpt

	#Get + Normalization 
	yaw_l,pitch_l,roll_l,list_name = adapt_all_curves(list_path,id_curve)
	#Choose plot
	if(id_curve==1): #pitch = f(yaw)
		title   = 'pitch = f(yaw)'
		angle_x_l = yaw_l
		angle_y_l = pitch_l	
		
	elif(id_curve==2):#roll = f(pitch)
		title   = 'roll = f(pitch)'
		angle_x_l = pitch_l
		angle_y_l = roll_l
	else:
		title   = 'yaw = f(roll)'
		angle_x_l = roll_l
		angle_y_l = yaw_l

	
	#Plot
	plb.rcParams['figure.figsize'] = 25, 10
	plb.subplots_adjust(hspace=0.5,wspace=0.5)
	number_of_subplots=len(list_path)
	
	for i,v in enumerate(xrange(number_of_subplots)):
	    v = v+1
	    ax1 = plb.subplot(number_of_subplots/2+1,2,v)
	    #Interpolate with B-Spline
	    x_spline,y_spline = interpolate_spline(angle_x_l[i], angle_y_l[i],id_curve)
	    ax1.plot(angle_x_l[i],angle_y_l[i],'r--',x_spline,y_spline)

	    title_plot = title + ' : ' + list_name[i] 

	    ax1.set_title(title_plot)
	    ax1.set_xlim([-0.5,1.5])
	    ax1.set_ylim([-0.5,1.5])
	try:
            os.mkdir('Plot_Spline')
        except OSError:
            pass
	try:
            os.mkdir('Plot_Spline/Spline_'+str(id_curve))
        except OSError:
            pass
	plt.savefig('Plot_Spline/Spline_'+str(id_curve)+'/'+title.replace(' = ','_').replace('(','_').replace(')',str(cpt)+'.png'))
	plt.close()



###################################################################
# ACP for OCSVM
def compute_acp(angle_x,angle_y,plot):
	
	pca = skd.PCA(n_components=2)
	pca.fit(np.array([angle_x,angle_y]).T)
	veps = pca.components_
	vep1 = veps[0,:]
	vep2 = veps[1,:]
	
	if plot:
		mean_x  = np.mean(angle_x)
		mean_y  = np.mean(angle_y)
		sigma_x = np.std(angle_x)
		sigma_y = np.std(angle_y)
		n	= len(angle_x)
		M_barre = np.array([[e-mean_x for e in angle_x],[e-mean_y for e in angle_y]]).T

		barycenter_x = np.mean(M_barre[:,0])
		barycenter_y = np.mean(M_barre[:,1])
		plt.plot(barycenter_x,barycenter_y,'ro')
		plt.plot(M_barre[:,0],M_barre[:,1])
		plt.quiver([barycenter_x,barycenter_x],[barycenter_y,barycenter_y],vep1,vep2,angles='uv',scale=5)
		plt.show()
	
	
	return vep1,vep2

#####################################################################
if __name__ == "__main__":

	l = []
	"""
	x = range(1,200)
	xr = range(1,199)[::-1]
	x.extend(xr)
	x.extend(x)
	x.extend(x)
	y = [1+random.uniform(-0.1,0.1) for i in range(len(x))]
	xs,ys = interpolate_spline(x,y,1,500)
	plt.plot(x,y,'r--',xs,ys)
	#plt.plot(l[0],l[1],'bo')
	plt.ylim(-2,2)
	plt.show()
	"""

	direct = '../bonnes_mesures/'
	list_dir = next(os.walk(direct))[1]
	list_dir = [direct+s for s in list_dir]
	list_path=[]
	for path in list_dir:
		list_path.extend(glob.glob(path+'/*.orpl'))
	for i in range(5,10):
		x,y,r = get_file_data(list_path[i])
		xs,ys = interpolate_spline(x,y,1,500)
		plt.plot(x,y,'r--',xs,ys)
		plt.plot(l[0],l[1],'bo')
		plt.show()

