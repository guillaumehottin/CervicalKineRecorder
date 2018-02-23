#####################################################################
#For this package, we work with three angles (Yaw,Pitch,Roll).
#We only use the yaw motion (horizontal variation) .
#We consider three  planes:
#    _Pitch = f(Yaw)    (We associate the id_curve number 1)
#    _Roll  = f(Pitch)  (id_curve 2)
#    _Roll   = f(Yaw)   (id_curve 3)
#This file permits to approximate the motion by a BSpline.
#For each oscillations, we compute control points and mean it.
#At the end, we get a mean Bspline of oscillations.
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

global plot,cpt, patho_stg

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


def detect_oscillations(diff_l,list_angle):
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
#Have same number of control points for each oscillations and compute mean
#Inputs:
#    _ oscillations_x : List of List with each oscillations for axis x
#    _ oscillations_y : Same with axis y
#Outputs:
#    _ Mean control points : Two lists
########################################################

def mean_control_points(oscillations_x,oscillations_y):
    #Get same number of points of each oscillations
    len_list = list(map(len, oscillations_x))
    min_len = min(len_list)    
    index = len_list.index(min_len)
        
    for i in range(len(oscillations_x)):
        if (i!=index):
            n = len(oscillations_x[i])
            oscillations_x[i] = [oscillations_x[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
            oscillations_y[i] = [oscillations_y[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
    
    mean_control_x = [float(sum(col))/len(col) for col in zip(*oscillations_x)]
    mean_control_y = [float(sum(col))/len(col) for col in zip(*oscillations_y)]
    return mean_control_x, mean_control_y


########################################################
# Compute mean control points for oscillations
# Detect each oscillations, get same number of points
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

    index_change_l = detect_oscillations(diff_l, angle_x)[::2]  
    #Build list for each oscillations
    oscillations_x, oscillations_y = [],[]
    for i in range(len(index_change_l)-1):
        oscillations_x += [angle_x[index_change_l[i]:index_change_l[i+1]+1]]
        oscillations_y += [angle_y[index_change_l[i]:index_change_l[i+1]+1]]

    oscillations_x += [angle_x[index_change_l[-1]:]]
    oscillations_y += [angle_y[index_change_l[-1]:]]
    
    #Mean
    mean_control_x, mean_control_y = mean_control_points(oscillations_x,oscillations_y)
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
    
    Returns++++++++++++++
    float, float
            Mean and standard deviation of the distance.
    """
    distances = []

    #Compute list of differences between two points
    diff_curve  = compute_difference_list_motion(curve[:,0])
    diff_spline = compute_difference_list_motion(spline[:,0])
    #Detect oscillations beginning
    index_change_curve  = detect_oscillations(diff_curve,curve[:,0])
    index_change_spline = detect_oscillations(diff_spline,spline[:,0])
    #Build multi points for splines
    one_way_spline = np.array(spline[:index_change_spline[-1]+1,:])
    return_spline  = np.array(spline[index_change_spline[-1]:,:])
    one_way_spline_mp = geo.MultiPoint(one_way_spline)
    return_spline_mp  = geo.MultiPoint(return_spline)

    #Compute distance for each oscillation
    for index in range(0,len(index_change_curve)-2,2):
        one_way_curve = np.array(curve[index_change_curve[index]:index_change_curve[index+1]+1,:])     
        return_curve  = np.array(curve[index_change_curve[index+1]:index_change_curve[index+2]+1,:])    
        for p in one_way_curve:
            distances += [distance_to_spline(p, one_way_spline_mp)]
        for p in return_curve:
            distances += [distance_to_spline(p, return_spline_mp)]
 
    one_way_curve = np.array(curve[index_change_curve[-2]:index_change_curve[-1]+1,:])     
    return_curve  = np.array(curve[index_change_curve[-1]:,:])    
    for p in one_way_curve:
        distances += [distance_to_spline(p, one_way_spline_mp)]
    for p in return_curve:
        distances += [distance_to_spline(p, return_spline_mp)]

    return np.mean(distances), np.std(distances)


def score_model(list_pts, npts):
    global plot, cpt, patho_stg
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
    angle_x,angle_y,xs,ys = interpolate_spline(list_pts,npts)
    spline = np.array(myutils.coord2points([xs, ys]))
    sd_distance = distance_curve_to_spline(list_pts, spline)[1]
    if plot:
        plt.plot(angle_x,angle_y,'r--',xs,ys,'b')
        plt.title('Standard deviation of distances : ' + str(sd_distance))
        plt.savefig('../Splines/spline_' + str(cpt)+'_'+patho_stg + '.png')
        cpt +=1
        plt.close()
    return sd_distance


def interpolate_spline(list_coord,nb_points=700,step=10):
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

    #Get data according to id_curve
    angle_x, angle_y = list_coord[:,0],list_coord[:,1]
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

    plot = True
    cpt = 0
    patho_stg = "patho"
    direct = '../gui/guillaume/'
    
    list_files = myutils.fetch_files(dir_name=direct,sub_dir='Normalized',extension='.txt')
    
    patho = []
    for i in range(len(list_files)):
        if "patho" in list_files[i]:
            patho.append(list_files[i])

    list_files = patho 
   
    list_all_points = np.array([myutils.get_coord(f) for f in list_files])

    npts = 150
    scores = []
    start_time = time.time()
    for i, list_coord in enumerate(list_all_points):
        list_points = myutils.coord2points(list_coord)
        #Only two angles : Yaw and Pitch
        list_points = np.array([list_points[k][:2] for k in range(len(list_points))])
        scores += [score_model(list_points, npts)]

        
    print("%s seconds" % (time.time() - start_time))
    print(scores)
    print(np.mean(scores))
