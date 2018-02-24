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


import numpy as np
from scipy import interpolate
import shapely.geometry as geo
import myutils


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

    return yaw_l, pitch_l, roll_l


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
    
    return index_change_l



########################################################
#Have same number of control points for each oscillation and compute mean
#Inputs:
#    _ two_ways_x : List of List with each two ways for axis x
#    _ two_ways_y : Same with axis y
#Outputs:
#    _ Mean control points : Two lists
########################################################

def mean_control_points(oscillations_x, oscillations_y):
#Get same number of points of each oscillation
    len_list = list(map(len, oscillations_x))
    min_len = min(len_list)    
    index = len_list.index(min_len)
        
    for i in range(len(oscillations_x)):
        if (i != index):
            n = len(oscillations_x[i])
            oscillations_x[i] = [oscillations_x[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
            oscillations_y[i] = [oscillations_y[i][int(j + j*(n-min_len)/min_len)] for j in range(min_len)]
    
    mean_control_x = [float(sum(col))/len(col) for col in zip(*oscillations_x)]
    mean_control_y = [float(sum(col))/len(col) for col in zip(*oscillations_y)]
    return mean_control_x, mean_control_y


########################################################
# Compute mean control points for oscillations
# Detect each oscillation, get same number of points
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

    index_change_l_res = detect_oscillations(diff_l, angle_x)  
    index_change_l = index_change_l_res[::2]
    #Build list for each oscillation
    oscillations_x, oscillations_y = [],[]
    for i in range(len(index_change_l)-1):
        oscillations_x += [angle_x[index_change_l[i]:index_change_l[i+1]+1]]
        oscillations_y += [angle_y[index_change_l[i]:index_change_l[i+1]+1]]

    oscillations_x += [angle_x[index_change_l[-1]:]]
    oscillations_y += [angle_y[index_change_l[-1]:]]
    
    #Mean
    mean_control_x, mean_control_y = mean_control_points(oscillations_x,oscillations_y)
    mean_control_x, mean_control_y = mean_control_x[::step], mean_control_y[::step]
    
    return mean_control_x, mean_control_y, index_change_l


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


def distance_curve_to_spline(curve, spline, indices_curve):
    """
    Compute the mean and standard deviation distance from a curve to a spline.
    
    Parameters
    ----------
    curve : array
            Array of points of the curve.
    spline : array
            Array of points of the spline.
    indices_curve : array
            Indices of the points of the curve when the motion changes way.
            
    Returns
    -------
    float, float
            Mean and standard deviation of the distance.
    """
    
    distances = []
    
    #Compute list of differences between two points
    diff_spline = compute_difference_list_motion(spline[:, 0])
    #Detect oscillations beginning
    index_change_spline = detect_oscillations(diff_spline, spline[:, 0])
    #Build multi points for splines
    forth_spline = np.array(spline[:index_change_spline[-1]+1])
    back_spline  = np.array(spline[index_change_spline[-1]:])
    forth_spline_mp = geo.MultiPoint(forth_spline)
    back_spline_mp  = geo.MultiPoint(back_spline)
    

    #Compute distance for each oscillation
    for index in range(0,len(indices_curve)-2,2):
        forth_curve = np.array(curve[indices_curve[index]:indices_curve[index+1]])     
        back_curve  = np.array(curve[indices_curve[index+1]:indices_curve[index+2]+1])    
        for p in forth_curve:
            distances += [distance_to_spline(p, forth_spline_mp)]
        for p in back_curve:
            distances += [distance_to_spline(p, back_spline_mp)]
 
    forth_curve = np.array(curve[indices_curve[-2]:indices_curve[-1]])    
    back_curve  = np.array(curve[indices_curve[-1]:])    
    for p in forth_curve:
        distances += [distance_to_spline(p, forth_spline_mp)]
    for p in back_curve:
        distances += [distance_to_spline(p, back_spline_mp)]
    
    return np.mean(distances), np.std(distances)


def score_model(list_coord, xs, ys, indices_change):
    """
    Compute a score, i.e. the standard deviation of the distance to the spline.
    
    Parameters
    ----------
    list_coord : array
            Array of coordinates.
    xs : array
            X-axis coordinates of the points of the mean spline.
    ys : array
            Y-axis coordinates of the points of the mean spline.
    indices_change : array
            Indices of the points of the curve where the motion changes way.
            
    Returns
    -------
    float
            Standard deviation of the distance from each point to the mean spline.
    """    
    spline = np.array(myutils.coord2points([xs, ys]))
    return distance_curve_to_spline(myutils.coord2points(list_coord), spline, indices_change)[1]


def interpolate_spline(list_coord,nb_points=700,step=20):
    """
    Compute control points and create the spline.
    
    Parameters
    ----------
    list_coord : array
            Array of two coordinates.
    nb_points : int
            Number of points in the spline.
    step : int
            Controls points are taken every step points.
    
    Returns
    -------            
    tuple of 3 arrays
            [0] is the x-axis coordinates of the spline
            [1] is the y-axis coordinates of the spline
            [2] is the indices of when the curve changes way
    """

    #Get data according to id_curve
    angle_x, angle_y = list_coord
    #1) Choose control points
    x_control, y_control, indices_change = get_control_points(angle_x, angle_y, step)
    #2)Interpolate
    #Inputs  :
    #    s: smoothing condition
    #Outputs : 
    #    tck : tuple (t,c,k) vector of knots, B-spline coeff and the degree
    #    u   : weighted sum of squared residuals of the approximation
    tck, u = interpolate.splprep([x_control, y_control], s=0.0)
    x_spline, y_spline = interpolate.splev(np.linspace(0, 1, nb_points), tck)

    return x_spline, y_spline, indices_change


def create_model(array_data):
    """
    Create the model for the variability of the distance to the mean spline.
    
    Parameters
    ----------
    array_data : array of arrays of arrays of float
            Each element is an array of coordinates.
    
    Returns
    -------
    float, float
            Mean standard deviation for pitch=f(yaw) and roll=f(yaw) respectively.
    """
    yaw_pitch = []
    yaw_roll = []
    for one_acq in array_data:
        p, r = myutils.get_axes(one_acq, ((1, 2), (1, 3)))
        yaw_pitch += [p]
        yaw_roll += [r]
    std_pitch = []
    std_roll = []
    npts = 150
    for i in range(len(yaw_pitch)):
        xsp, ysp, indices_p = interpolate_spline(yaw_pitch[i], npts)
        xsr, ysr, indices_r = interpolate_spline(yaw_roll[i], npts)
        std_pitch += [score_model(yaw_pitch[i], xsp, ysp, indices_p)]
    print(std_pitch)
    #We use the mean for now, but might take a quantile or other measure later.
    return np.mean(std_pitch), np.mean(std_roll)
    

if __name__ == "__main__":
    
    direct = 'data/guillaume2/'
    
    list_dir = ['data/guillaume2/Normalized']
    list_coord = myutils.fetch_from_dirs(list_dir)
    #TODO: ON THE FLY NORMALIZATION

    npts = 150
    
    p, r = create_model(list_coord)
        
    