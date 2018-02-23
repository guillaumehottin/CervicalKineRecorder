#####################################################################
#For this package, we work with three angles (Yaw,Pitch,Roll).
#We only use the yaw motion (horizontal variation) .
#We consider three  planes:
#    _Pitch = f(Yaw)    (We associate the id_curve number 1)
#    _Roll  = f(Pitch)  (id_curve 2)
#    _Roll   = f(Yaw)   (id_curve 3)
#This file permits to approximate the motion by a BSpline.
#For each two ways, we compute control points and mean it.
#At the end, we get a mean Bspline of two ways.
#We can also do an ACP for a classification (type OCSVM)
#####################################################################


import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import interpolate
from plot_save import normalize
import glob
import shapely.geometry as geo
import myutils
import time

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


########################################################
#Compute distance between two consecutives points
#for the main axis of motion
#For yaw motion -> Main axis = yaw
########################################################
def compute_difference_list_motion(angle_x):
    return [angle_x[i]-angle_x[i+1] for i in range(len(angle_x)-1)]
            

def positive_values(array):
    """
    Number of positive values in an array-like.
    
    Parameters
    ----------
    array : array
            The array.
    
    Returns
    -------
    int
    """
    n = 0
    for i in array:
        if i >= 0:
            n += 1
    return n


def detect_back_for(diff_l,list_angle):
    """
    Detect when a movement changes its way.
    
    Parameters
    ----------
    diff_l : array
            Array of the differences between consecutive elements. The result of
            the function is based on the sign of its elements.
    list_angle : array
            Array of corresponding coordinates.
            
    Returns
    -------
    array of int
            Indices of the elements where the movement changes its way.
    """
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

def get_control_points(angle_x, angle_y, step):

    #Compute difference between two consecutives points    
    diff_l = compute_difference_list_motion(angle_x)

    index_change_l = detect_back_for(diff_l, angle_x)[::2]  
    #Build list for each two ways
    two_ways_x, two_ways_y = [],[]
    for i in range(len(index_change_l)-1):
        two_ways_x += [angle_x[index_change_l[i]:index_change_l[i+1]+1]]
        two_ways_y += [angle_y[index_change_l[i]:index_change_l[i+1]+1]]

    two_ways_x += [angle_x[index_change_l[-1]:]]
    two_ways_y += [angle_y[index_change_l[-1]:]]
    
    #Mean
    mean_control_x, mean_control_y = mean_control_points(two_ways_x,two_ways_y)
    mean_control_x, mean_control_y = mean_control_x[::step], mean_control_y[::step]
    
    return mean_control_x,mean_control_y


def distance_to_spline(pt, spline):
    """
    Compute the euclidean distance of a point to a spline.
    
    Parameters
    ----------
    pt : array
            Array/list/tuple of two coordinates.
    spline : MultiPoint
            Points which make the spline.
    
    Returns
    -------
    float
            Distance from the point to the spline.
    """
    point = geo.Point(pt)
    return point.distance(spline)


def distance_curve_to_spline(curve, spline):
    """
    Compute the mean and standard deviation distance from a curve to a spline.
    
    Parameters
    ----------
    curve : array
            Array of points of the curve.
    spline : array
            Array of points of the spline.
    
    Returns
    float, float
            Mean and standard deviation of the distance.
    """
    distances = []
    spline_mp = geo.MultiPoint(spline)
    for p in curve:
        distances += [distance_to_spline(p, spline_mp)]
    return np.mean(distances), np.std(distances)


def score_model(list_pts, npts):
    """
    Compute a score, i.e. the standard deviation of the distance to the spline.
    
    Parameters
    ----------
    list_pts : array
            Array of points.
    x_spline : array
            X-axis coordinates of the points of the mean spline.
    y_spline : array
            Y-axis coordinates of the points of the mean spline.
    npts : int
            Number of points in the spline.
    
    Returns
    -------
    float
            Standard deviation of the distance from each point to the mean spline.
    """
    angle_x,angle_y,xs,ys = interpolate_spline(list_pts,1,npts)
    spline = myutils.coord2points([xs, ys])
    return distance_curve_to_spline(list_pts, spline)[1]


def interpolate_spline(list_coord,nb_points=700,step=20):
    """
    Compute control points and create the spline.
    
    Parameters
    ----------
    list_points : array
            Array of points.
    id_curve : int
            1 for pitch = f(yaw), 2 for roll = f(pitch), 3 for roll = f(yaw)
    nb_points : int
            Number of points in the spline.
    step : int
            Controls points are taken every step points.
    
    Returns
    -------            
    tuple of 4 arrays
            [0] is the x-axis coordinates of the curve
            [1] is the y-axis coordinates of the curve
            [2] is the x-axis coordinates of the spline
            [3] is the y-axis coordinates of the spline
    """
    global l

    #Get data according to id_curve
    angle_x, angle_y = list_coord
    #1) Choose control points
    x_control, y_control = get_control_points(angle_x, angle_y, step)
    l = [x_control, y_control]
    #2)Interpolate
    #Inputs  :
    #    s: smoothing condition
    #Outputs : 
    #    tck : tuple (t,c,k) vector of knots, B-spline coeff and the degree
    #    u   : weighted sum of squared residuals of the approximation
    tck, u = interpolate.splprep([x_control, y_control], s=0.0)
    x_spline, y_spline = interpolate.splev(np.linspace(0, 1, nb_points), tck)

    return angle_x, angle_y, x_spline, y_spline


#####################################################################
if __name__ == "__main__":

    l = []
    ll,lr = [],[]
    
    direct = 'data/guillaume2/'
    
    list_files = myutils.fetch_files(dir_name=direct,sub_dir='Normalized',extension='.orpl')
    list_all_points = np.array([myutils.get_coord(f) for f in list_files])

    npts = 150
    scores = []
    start_time = time.time()
    for i, list_coord in enumerate(list_all_points):
        list_points = myutils.coord2points(list_coord)
        scores += [score_model(list_points, npts)]
        #Interpolate curve
        """
        angle_x,angle_y,xs,ys = interpolate_spline(list_points,1,npts)
        #Plot
        plt.plot(angle_x,angle_y,'r--',xs,ys)
        plt.plot(l[0],l[1],'bo')
        plt.plot(np.array(angle_x)[ll],np.array(angle_y)[ll],'go')
        plt.plot(np.array(angle_x)[lr],np.array(angle_y)[lr],'yo')
        plt.savefig(direct+'Splines/spline_nb_'+str(i)+'.png')
        plt.close()
        """
        
    print("%s seconds" % (time.time() - start_time))
    print(scores)
    print(np.mean(scores))