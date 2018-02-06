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

#####################################################################
#Symmetric
def need_symmetric(angle_yaw,angle_pitch,angle_roll,id_curve):
	if (id_curve==1):
		return need_symmetric_pitch_yaw(angle_yaw,angle_pitch)
	elif (id_curve==2):
		return need_symmetric_roll_pitch(angle_pitch,angle_roll)
	else:
		return need_symmetric_yaw_roll(angle_roll,angle_yaw)


def need_symmetric_pitch_yaw(angle_x,angle_y):
	positive_l,negative_l = [],[]
	positive_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_x[i]>0.5]
	negative_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_x[i]<0.5]
	if(max(positive_l)>max(negative_l)):
		return False
	else:
		return True

def need_symmetric_roll_pitch(angle_x,angle_y):
	positive_l,negative_l = [],[]
	positive_l = [angle_x[i] for i in range(0,len(angle_y)) if angle_y[i]>0.5]
	negative_l = [angle_x[i] for i in range(0,len(angle_y)) if angle_y[i]<0.5]
	if(max(positive_l)>max(negative_l)):
		return False
	else:
		return True

def need_symmetric_yaw_roll(angle_x,angle_y):
	"""
	positive_l,negative_l = [],[]
	positive_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_y[i]>0.51]
	negative_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_y[i]<0.51]
	"""
	l = [angle_y[i] for i in range(0,len(angle_y)) if angle_x[i]>0.49 and angle_x[i]<0.51]
	if(np.max(l)<0.5):
		return False
	else:
		return True
####################################################################################"
#Transformation	
	
def adapt_orientation(angle_yaw,angle_pitch,angle_roll,id_curve):
	modify = False
	if(need_symmetric(angle_yaw,angle_pitch,angle_roll,id_curve)):
		modify=True
		if (id_curve==1):
			return [y * -1 +1 for y in angle_yaw],angle_pitch,angle_roll,modify
		elif (id_curve==2):
			return angle_yaw,angle_pitch,[y * -1 +1 for y in angle_roll],modify
		else:
			return [y * -1 +1 for y in angle_yaw],angle_pitch,[y * -1 +1 for y in angle_roll],modify
		 
	else:
		return angle_yaw,angle_pitch,angle_roll,modify



def adapt_all_curves(list_path,id_curve):
	yaw_l,pitch_l,roll_l = [],[],[]
	list_name = []
	list_sym = []
	
	for path in list_path:	
		yaw,pitch,roll  = get_file_data(path)
		yaw,pitch,roll  = normalize(yaw,pitch,roll)
		yaw,pitch,roll,modify  = adapt_orientation(yaw,pitch,roll,id_curve)
		yaw_l.append(yaw)
		pitch_l.append(pitch)
		roll_l.append(roll)
		list_name.append(path.split('/')[1])
		list_sym.append(modify)

	return yaw_l,pitch_l,roll_l,list_name,list_sym

def prepare_interpolation(id_curve,yaw_l,pitch_l,roll_l):
	all_control_x = []
	all_control_y = []

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

	return angle_x,angle_y,all_control_x, all_control_y,title

def plot_example(list_path,id_curve,index_interpolate_data):
	global cpt
	#Normalization + Symmetric if necessary
	yaw_l,pitch_l,roll_l,list_name,list_sym = adapt_all_curves(list_path,id_curve)
	
	#Get all control points
	angle_x,angle_y,all_control_x, all_control_y,title = prepare_interpolation(id_curve,yaw_l,pitch_l,roll_l)

	#Interpolate with B-Spline
	tck,u=interpolate.splprep([all_control_x[index_interpolate_data],all_control_y[index_interpolate_data]],s=0.0)
	x_spline,y_spline= interpolate.splev(np.linspace(0,1,100),tck)	
	
	#Plot
	plb.rcParams['figure.figsize'] = 25, 10
	plb.subplots_adjust(hspace=0.5,wspace=0.5)
	number_of_subplots=len(list_path)
	
	for i,v in enumerate(xrange(number_of_subplots)):
	    v = v+1
	    ax1 = plb.subplot(number_of_subplots/2+1,2,v)
	    ax1.plot(angle_x[i],angle_y[i],'r--',x_spline,y_spline)
	    title_plot = title + ' : ' + list_name[i] + ' (Spline ' + str(index_interpolate_data) + ') '
	    if (list_sym[i]):
		title_plot += ' (Sym) '
	    ax1.set_title(title_plot)
	    ax1.set_xlim([-0.5,1.5])
	    ax1.set_ylim([-0.5,1.5])
	try:
            os.mkdir('Plot_Spline')
        except OSError:
            pass
	try:
            os.mkdir('Plot_Spline/Spline_'+str(list_name[index_interpolate_data]))
        except OSError:
            pass
	plt.savefig('Plot_Spline/Spline_'+str(list_name[index_interpolate_data])+'/'+title.replace(' = ','_').replace('(','_').replace(')',str(cpt)+'.png'))
	plt.close()



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


"""
direct = '../bonnes_mesures/'
list_dir = next(os.walk(direct))[1]
list_dir = [direct+s for s in list_dir]
list_path=[]
for path in list_dir:
	list_path.extend(glob.glob(path+'/*.orpl'))

cpt = 0
list_path = [list_path[1]]
for index in range(len(list_path)):

	print "Iteration " + str(index+1)+'/'+str(len(list_path))
	plot_example(list_path,1,index)
	plot_example(list_path,2,index)
	plot_example(list_path,3,index)
	cpt+=1

	y,p,r = get_file_data(list_path[index])
	vep1,vep2 = compute_acp(y,p,True)
	vep1,vep2 = compute_acp(p,r,True)
	vep1,vep2 = compute_acp(r,y,True)
"""
