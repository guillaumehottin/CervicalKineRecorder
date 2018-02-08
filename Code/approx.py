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
from hausdorff import hausdorff

global cpt 

def get_file_data(path):
	f = open(path,"r")
	data = f.readlines()
	yaw_l, pitch_l, roll_l = [],[],[]
	data.pop(0)

	#Ignore data with not enough points

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


def get_control_points(angle_x,angle_y):
	return angle_x[::3], angle_y[::3]


#####################################################################
def interpolate_spline(angle_x,angle_y):
	#1) Choose control points
	x_control,y_control = get_control_points(angle_x,angle_y)

	#2)Interpolate
	#Inputs  :
	#	s: smoothing condition
	#Outputs : 
	#	tck : tuple (t,c,k) vector of knots, B-spline coeff and the degree
	#	u   : weighted sum of squared residuals of the approximation
	tck,u=interpolate.splprep([x_control,y_control],s=0.0)
	x_spline,y_spline= interpolate.splev(np.linspace(0,1,100),tck)

	return x_spline,y_spline


####################################################################################
#Transformation	
	
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

def prepare_interpolation(id_curve,yaw_l,pitch_l,roll_l):
	all_control_x = []
	all_control_y = []

	#Choose plot
	if(id_curve==1): #pitch = f(yaw)
		angle_x = yaw_l
		angle_y = pitch_l
		title   = 'pitch = f(yaw)'	
		for i in range(len(yaw_l)):
			c_x,c_y = get_control_points(yaw_l[i],pitch_l[i])
			all_control_x.append(c_x)
			all_control_y.append(c_y)

	elif(id_curve==2):#roll = f(pitch)
		angle_x = pitch_l
		angle_y = roll_l
		title   = 'roll = f(pitch)'
		for i in range(len(pitch_l)):
			c_x,c_y = get_control_points(pitch_l[i],roll_l[i])
			all_control_x.append(c_x)
			all_control_y.append(c_y)
	else:
		angle_x = roll_l
		angle_y = yaw_l
		title   = 'yaw = f(roll)'
		for i in range(len(yaw_l)):
			c_x,c_y = get_control_points(roll_l[i],yaw_l[i])
			all_control_x.append(c_x)
			all_control_y.append(c_y)

	n = len(all_control_x)

	#Truncate to have same number of points in each list
	min_l = min(map(len, all_control_x))
	all_control_x = [all_control_x[i][:min_l] for i in range(n)]
	all_control_y = [all_control_y[i][:min_l] for i in range(n)]

	#Mean Control Points
	all_control_x,all_control_y = np.array(all_control_x),np.array(all_control_y)
	mean_control_x,mean_control_y = [float(sum(col))/len(col) for col in zip(*all_control_x)],[float(sum(col))/len(col) for col in zip(*all_control_y)]
	return angle_x,angle_y,mean_control_x,mean_control_y,title


#Compute Hausdorff distance
def hausdorff_distance(curve1,curve2):
	d = hausdorff(curve1,curve2)
	return d

#################################################################################
## Script plots
def plot_example(list_path,id_curve):
	global cpt
	#Get + Normalization 
	yaw_l,pitch_l,roll_l,list_name = adapt_all_curves(list_path,id_curve)
	
	#Get control points
	angle_x,angle_y,mean_control_x, mean_control_y,title = prepare_interpolation(id_curve,yaw_l,pitch_l,roll_l)

	#Interpolate with B-Spline
	tck,u=interpolate.splprep([mean_control_x, mean_control_y],s=0.0)
	x_spline,y_spline= interpolate.splev(np.linspace(0,1,100),tck)	
	
	#Plot
	plb.rcParams['figure.figsize'] = 25, 10
	plb.subplots_adjust(hspace=0.5,wspace=0.5)
	number_of_subplots=len(list_path)
	
	for i,v in enumerate(xrange(number_of_subplots)):
	    v = v+1
	    ax1 = plb.subplot(number_of_subplots/2+1,2,v)
	    ax1.plot(angle_x[i],angle_y[i],'r--',x_spline,y_spline)

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



direct = '../bonnes_mesures/'
list_dir = next(os.walk(direct))[1]
list_dir = [direct+s for s in list_dir]
list_path=[]
for path in list_dir:
	list_path.extend(glob.glob(path+'/*.orpl'))
cpt = 0
list_path = list_path[:6]


plot_example(list_path,1)
plot_example(list_path,2)
plot_example(list_path,3)
cpt+=1
"""
for index in range(len(list_path)):
	y,p,r = get_file_data(list_path[index])
	vep1,vep2 = compute_acp(y,p,True)
	vep1,vep2 = compute_acp(p,r,True)
	vep1,vep2 = compute_acp(r,y,True)
"""

