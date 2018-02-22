#####################################################################
#For this package, we work with three angles (Yaw,Pitch,Roll).
#We only use the yaw motion (horizontal variation) .
#We consider three  planes:
#    _Pitch = f(Yaw)    (We associate the id_curve number 1)
#    _Roll  = f(Pitch)  (id_curve 2)
#    _Yaw   = f(Roll)   (id_curve 3)
#This file permits to approximate the motion by a BSpline.
#For each two ways, we compute control points and mean it.
#At the end, we get a mean Bspline of two ways.
#We can also do an ACP for a classification (type OCSVM)
#####################################################################


import matplotlib.pyplot as plt
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
from mpl_toolkits.mplot3d import Axes3D

global cpt ,l,ll,lr

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
# Get data in list_path and normalize it
# Inputs:
#     _ list_path: List
#     _ id_curve: int
#Outputs:
#     _ List of List with all angles : ith element = (yaw_i,pitch_i,roll_i)
#     _ list_name : List with names of all patients
########################################################
    
def get_normalize_curves(list_path):
    list_all_points = []
    list_name = []
    list_sym = []
    
    for path in list_path:    
        #Get data and normalize it
        yaw,pitch,roll  = get_file_data(path)
        yaw,pitch,roll  = normalize(yaw,pitch,roll)
        list_points = [(yaw[j],pitch[j],roll[j]) for j in range(len(yaw))]
        list_all_points += [list_points]
        list_name.append(path.split('/')[1])

    return list_all_points,list_name



##################################################################
#We consider three  planes:
#    _Pitch = f(Yaw)    (We associate the id_curve number 1)
#    _Roll  = f(Pitch)  (id_curve 2)
#    _Yaw   = f(Roll)   (id_curve 3)
# It extracts adapted points according to id_curve
#Input : list_points : list [..., (yaw,pitch,roll), ...]
##################################################################

def get_points_curve(list_points,id_curve):
    if(id_curve==1):
        angle_x = [list_points[i][0] for i in range(len(list_points))]
        angle_y = [list_points[i][1] for i in range(len(list_points))]
    elif(id_curve==2):
        angle_x = [list_points[i][1] for i in range(len(list_points))]
        angle_y = [list_points[i][2] for i in range(len(list_points))]
    elif(id_curve==3):
        angle_x = [list_points[i][2] for i in range(len(list_points))]
        angle_y = [list_points[i][0] for i in range(len(list_points))]
    else:
        angle_x = []
        angle_y = []
    return angle_x,angle_y

########################################################
#Compute distance between two consecutives points
#for the main axis of motion
#For yaw motion -> Main axis = yaw
########################################################
def compute_difference_list_motion(angle_x,angle_y,id_curve):
    if(id_curve==1 ):  
        #Detect two ways
        diff_l = [angle_x[i]-angle_x[i+1] for i in range(len(angle_x)-1)]
            
    elif(id_curve==2 or id_curve==3):#Roll = f(pitch)
        diff_l = [angle_y[i]-angle_y[i+1] for i in range(len(angle_y)-1)]
    else:          
        diff_l = []
    return diff_l


def positive_values(array):
    n = 0
    for i in array:
        if i >= 0:
            n += 1
    return n

########################################################
# Detect each two ways
# Input:
#     _ diff : List of differences between 2 consecutives points
# Output:
#     _ List with indexes for all two ways beginning
########################################################

def detect_two_ways(diff_l,list_angle):
    global ll,lr
    window_size = 20
    sign_l = np.sign(diff_l)
    index_change_l = [0]
    
    i = window_size
    while i < len(sign_l)-window_size:
        if list_angle[i]<0.2 or list_angle[i]>0.8:
            prev_array = diff_l[i-window_size:i]
            next_array = diff_l[i:i+window_size]
            prev_pos = positive_values(prev_array)
            next_pos = positive_values(next_array)
            if (prev_pos > window_size/2 and next_pos < window_size/2) or (prev_pos < window_size/2 and next_pos > window_size/2):
                index_change_l.append(i)
                i += window_size
            else:
                i += 1
        else:
            i += 1
    ll = list(index_change_l)[1:][::2]
    index_change_l = index_change_l[::2]
    lr = index_change_l
    
    return index_change_l



########################################################
#Have same number of control points for each two ways and compute mean
#Inputs:
#    _ two_ways_x : List of List with each two ways for axis x
#    _ two_ways_y : Same with axis y
#Outputs:
#    _ Mean control points : Two lists
########################################################

def mean_control_points(two_ways_x,two_ways_y):
#Get same number of points of each two ways
    len_list = list(map(len, two_ways_x))
    min_len = min(len_list)    
    index = len_list.index(min_len)
        
    for i in range(len(two_ways_x)):
        if (i!=index):
            n = len(two_ways_x[i])
            two_ways_x[i] = [two_ways_x[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
            two_ways_y[i] = [two_ways_y[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
    
    mean_control_x = [float(sum(col))/len(col) for col in zip(*two_ways_x)]
    mean_control_y = [float(sum(col))/len(col) for col in zip(*two_ways_y)]
    return mean_control_x, mean_control_y


########################################################
# Compute mean control points for two ways
# Detect each two ways, get same number of points
# and mean each list
# Inputs:
#     _ angle_x : List
#     _ angle_y : List
#     _ id_curve: int
#Outputs:
#     _ Control points
########################################################

def get_control_points(angle_x,angle_y,id_curve,step):


    #Compute difference between two consecutives points    
    diff_l = compute_difference_list_motion(angle_x,angle_y,id_curve)

    #Two ways
    if(id_curve==1 ):
        list_angle = angle_x
    else:
        list_angle = angle_y

    index_change_l = detect_two_ways(diff_l,list_angle)    
    #Build list for each two ways
    two_ways_x, two_ways_y = [],[]
    for i in range(len(index_change_l)-1):
        two_ways_x += [angle_x[index_change_l[i]:index_change_l[i+1]]]
        two_ways_y += [angle_y[index_change_l[i]:index_change_l[i+1]]]
        #Add point to have : end two_ways nb 1 == beginning two_ways nb 2
        two_ways_x[-1].append(angle_x[index_change_l[i+1]])
        two_ways_y[-1].append(angle_y[index_change_l[i+1]])

    two_ways_x += [angle_x[index_change_l[-1]:]]
    two_ways_y += [angle_y[index_change_l[-1]:]]
    
    #Mean
    mean_control_x, mean_control_y = mean_control_points(two_ways_x,two_ways_y)
    mean_control_x, mean_control_y = mean_control_x[::step], mean_control_y[::step]
    
    return mean_control_x,mean_control_y



########################################################
# Compute control points and Interpolate data
# Inputs:
#     _ list_points : List of points
#     _ id_curve: int
#Outputs:
#     _ Spline curve
########################################################

def interpolate_spline(list_points,id_curve,nb_points=700,step=20):
    global l

    #Get data according to id_curve
    angle_x,angle_y = get_points_curve(list_points,id_curve)
    #1) Choose control points
    x_control,y_control = get_control_points(angle_x,angle_y,id_curve,step)
    l = [x_control,y_control]
    #2)Interpolate
    #Inputs  :
    #    s: smoothing condition
    #Outputs : 
    #    tck : tuple (t,c,k) vector of knots, B-spline coeff and the degree
    #    u   : weighted sum of squared residuals of the approximation
    tck,u=interpolate.splprep([x_control,y_control],s=0.0)
    x_spline,y_spline= interpolate.splev(np.linspace(0,1,nb_points),tck)

    return angle_x,angle_y,x_spline,y_spline




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
        n    = len(angle_x)
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
    ll,lr = [],[]
    
    direct = 'data/guillaume2/'
    """
    list_dir = next(os.walk(direct))[1]
    list_dir = [direct+s for s in list_dir]
    """
    list_path=[]
    #Get all paths for orpl files
    #for path in list_dir:
    list_path.extend(glob.glob(direct+'/*.orpl'))
    #Get all data
    list_all_points,names = get_normalize_curves(list_path)

    try:
        os.mkdir(direct+'Splines')
    except FileExistsError:
        pass

    for i in range(len(list_path)):
        #Get ith list of points
        list_points = list_all_points[i]
        #Interpolate curve
        angle_x,angle_y,xs,ys = interpolate_spline(list_points,1,500)
        #Plot
        plt.plot(angle_x,angle_y,'r--',xs,ys)
        plt.plot(l[0],l[1],'bo')
        plt.plot(np.array(angle_x)[ll],np.array(angle_y)[ll],'go')
        plt.plot(np.array(angle_x)[lr],np.array(angle_y)[lr],'yo')
        plt.savefig(direct+'Splines/spline_nb_'+str(i)+'.png')
        plt.close()
