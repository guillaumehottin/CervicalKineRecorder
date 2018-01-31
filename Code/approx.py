import matplotlib.pyplot as plt
import numpy as np
import os
import math
import numpy as np
from scipy.misc import comb
from scipy import interpolate
from pylab import subplots_adjust,subplot
from plot_save import normalize


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

############################################################################""


def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals



def interpolate_bezier(angle_x,angle_y,n_times):
	#1) Choose control points
	x_control,y_control = get_control_points(angle_x,angle_y)
	
	#2)Build Bezier curve
	m_control = np.zeros((len(x_control),2))
	for i in range(0,len(x_control)):
		m_control[i,:] = [x_control[i],y_control[i]]
	x_bezier,y_bezier = bezier_curve(m_control, n_times)

	return x_bezier,y_bezier

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
	positive_l = [angle_x[i] for i in range(0,len(angle_y)) if angle_y[i]>0.5]
	negative_l = [angle_x[i] for i in range(0,len(angle_y)) if angle_y[i]<0.5]
	if(max(positive_l)>max(negative_l)):
		return False
	else:
		return True

def need_symmetric_roll_pitch(angle_x,angle_y):
	positive_l,negative_l = [],[]
	positive_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_y[i]>0.5]
	negative_l = [angle_y[i] for i in range(0,len(angle_y)) if angle_y[i]<0.5]
	if(max(positive_l)>max(negative_l)):
		return False
	else:
		return True

def need_symmetric_yaw_roll(angle_x,angle_y):
	return False
	
	
def adapt_orientation(angle_yaw,angle_pitch,angle_roll,id_curve):

	if(need_symmetric(angle_yaw,angle_pitch,angle_roll,id_curve)):
		if (id_curve==1):
			return angle_yaw,[y * -1 for y in angle_pitch],angle_roll
		elif (id_curve==2):
			return angle_yaw,angle_pitch,[y * -1 for y in angle_roll]
		else:
			return angle_yaw,angle_pitch,angle_roll
		 
	else:
		return angle_yaw,angle_pitch,angle_roll

def plot_example(list_path,id_curve):
	yaw_l,pitch_l,roll_l = [],[],[]
	for path in list_path:	
		yaw,pitch,roll  = get_file_data(path)
		yaw,pitch,roll  = normalize(yaw,pitch,roll)
		yaw,pitch,roll  = adapt_orientation(yaw,pitch,roll,id_curve)
		yaw_l.append(yaw)
		pitch_l.append(pitch)
		roll_l.append(roll)

	if(id_curve==1): #pitch = f(yaw)
		angle_x = yaw_l
		angle_y = pitch_l
		title   = 'pitch = f(yaw)'	
		control_x,control_y = get_control_points(yaw_l[0],pitch_l[0])

	elif(id_curve==2):#roll = f(pitch)
		angle_x = pitch_l
		angle_y = roll_l
		title   = 'roll = f(pitch)'
		control_x,control_y = get_control_points(pitch_l[0],roll_l[0])
	else:
		angle_x = roll_l
		angle_y = yaw_l
		title   = 'yaw = f(roll)'
		control_x,control_y = get_control_points(roll_l[0],yaw_l[0])
	
	tck,u=interpolate.splprep([control_x,control_y],s=0.0)
	x_spline,y_spline= interpolate.splev(np.linspace(0,1,100),tck)	

	#Plot
	subplots_adjust(hspace=0.000)
	number_of_subplots=len(list_path)

	for i,v in enumerate(xrange(number_of_subplots)):
	    v = v+1
	    ax1 = subplot(number_of_subplots,1,v)
	    ax1.plot(angle_x[i],angle_y[i],'r--',x_spline,y_spline)
	    ax1.set_title(title + ' : Jeu de donnees ' + str(i))
	    ax1.set_xlim([0,1])
	    ax1.set_ylim([0,1])
	plt.show()

#####################################################################
file_1 = "Fri Sep 29 15_52_35 2017 - Lacet.orpl"
name_1 = "Aslanyan_Marine_23"

file_2 = "Fri Dec  8 15_10_38 2017 - Lacet.orpl"
name_2 = "bonnemaison_elodie_22"

file_3 = "Fri Oct  6 17_57_57 2017 - Lacet.orpl"
name_3 = "Marine_Lepetit_22"
list_path = ['bonnes_mesures/'+name_1+'/'+file_1,'bonnes_mesures/'+name_2+'/'+file_2,'bonnes_mesures/'+name_3+'/'+file_3]

plot_example(list_path,1)
plot_example(list_path,2)
plot_example(list_path,3)
