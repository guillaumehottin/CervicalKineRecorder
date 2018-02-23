import random as rd
import shutil
import shapely.geometry as geometry
import numpy as np
import os
import time
from shapely.wkt import loads

#Generate clusters based on their center and radius
def generate_clusters(centers,radii,npts_by_cluster):
    """
    Generate clusters of a specified number of points based on their centers and 
    radii. The repartition is done randomly around the center.
    
    Parameters
    ----------
    centers : array of 2-array of real
            The list of centers coordinates.
    radii : array of real
            The list of radii of the clusters. Must have the same length as centers.
    npts_by_cluster : int
            Number of points by cluster.
        
    Returns
    -------
    tuple 
            (x, y, pts) : x and y are lists containing all x-axis and y-axis 
            coordinates, respectively. 
            pts is a list of the points coordinates
    """
    if len(centers) != len(radii):
        raise ValueError('centers and radii must have the same length.')
    pts = []
    x = []
    y = []
    for j in range(len(radii)):
        xj = centers[j][0]
        yj = centers[j][1]
        rj = radii[j]
        for i in range(npts_by_cluster):
            theta = rd.random()*2*np.pi
            mod = rd.random()
            xi = xj+rj*mod*np.cos(theta)
            yi = yj+rj*mod*np.sin(theta)
            x.append(xi)
            y.append(yi)
            pts.append([xi,yi])
    return x,y,pts

#Generate n MultiPoints which consists of randomly generated clusters
def generate_MP(n,cl_min=1,cl_max=5,axes=[-10,10,-10,10],rmax=5,npts_by_clusters=20,alpha=0.7):
    res = []
    for i in range(n):
        nb_clusters = rd.randint(cl_min,cl_max)
        centers = []
        radii = []
        points = []
        for j in range(nb_clusters):
            centers += [[rd.randint(axes[0]+rmax,axes[1]-rmax),rd.randint(axes[2]+rmax,axes[3]-rmax)]]
            radii += [rd.randint(1,rmax)]
            _,_,pts = generate_clusters(centers,radii,npts_by_clusters)
            points += pts
        res += [array2MP(points)]
    return res

# Removes all subdirectories of curr_dir whose name is dir2rm
def remove_dir(curr_dir,dir2rm):
	list_dir = [x[0] for x in os.walk(curr_dir)]
	for name_dir in list_dir:
		if dir2rm in name_dir:
			shutil.rmtree(name_dir)
            
#Cast array of points to MultiPoint
def array2MP(pts):
    points = [geometry.asPoint(p) for p in pts]
    return geometry.MultiPoint(list(points))


def get_axes(list_coord, axes):
    """
    Get the coordinates of certain axes.
    
    Parameters
    ----------
    list_coord : array
            List of coordinates.
    axes : tuple of tuples of int
            Axes which need to be taken.
    
    Returns
    -------
    list of list of array of float
    """
    res = []
    for i,j in axes:
        res += [[list_coord[i-1], list_coord[j-1]]]
    return res
    
def check_letter(x):
    return x == 'f' or x == 'e' or x == 'd'

#Define RGBA color
def RGBA_arg():
    hex_str = hex(int(rd.random()*16777215))[2:]
    hex_str = 'ffefdf'
    n = len(hex_str)
    while n < 6:
        hex_str = '0'+hex_str
        n = len(hex_str)
    if check_letter(hex_str[0]) and check_letter(hex_str[2]) and check_letter(hex_str[4]):
        print('ok')
        index = 2*rd.randint(0,2)
        res_str = ''
        for i in range(len(hex_str)):
            if i == index:
                char = str(rd.randint(0,9))
            else:
                char = hex_str[i]
            res_str += char
        hex_str = res_str
    return '#'+hex_str
    
#To fetch files in a specified folder, returns the list of the paths to theses files
def fetch_files(dir_name='.',extension='.orpl',sub_dir=''):
    res = []
    path = dir_name+sub_dir
    for file in os.listdir(path):
        if extension in file:
            res += [path+'/'+file] 
    return res


def fetch_from_dirs(list_dir, extension='.orpl', sub_dir=''):
    list_coord = []
    for folder in list_dir:
        files = fetch_files(folder, extension, sub_dir)
        for f in files:
            list_coord += [get_coord(f)]
    return list_coord


#Get list of coordinates in an ORPL file (yaw,pitch_roll)
def get_coord(file_path):
    with open(file_path,"r") as f:
        data = f.readlines()
        
    yaw_l, pitch_l, roll_l = [], [], []

    data.pop(0)
    for i in range(len(data)):
        elems = data[i].split(" ")
        yaw_l.append(elems[0])
        pitch_l.append(elems[1])
        roll_l.append(elems[2])

    pitch_l = np.array(list(map(float, pitch_l)))
    yaw_l = np.array(list(map(float, yaw_l)))
    roll_l = np.array(list(map(float, roll_l)))

    return (yaw_l, pitch_l, roll_l)

#Convert n lists of m coordinates into a list of m n-dimensional vectors
def coord2points(data):
    n = len(data)
    m = len(data[0])
    points = []
    for i in range(m):
        point = []
        for j in range(n):
            point += [data[j][i]]
        points += [point]
    return points

def mean_succ_diff(data):
    """
    The mean difference beween successive elements of an array.
    
    Parameters
    ----------
    data : array
            The elements.
    
    Returns
    -------
    int
            The mean difference.
    """
    n = len(data)
    s=0
    for i in range(n-1):
        s += abs(data[i]-data[i+1])
    return s/(n-1)

def start_movement_index(data,motion,alpha=1,window_width=5):
    """
    A simple estimation of the beginning of the movement, based on the difference 
    between two successive points and a threshold.
    
    Parameters
    ----------
    data : array
            The data in the form of (yaw, pitch, roll).
    motion : str
            'Lacet', 'Roulis' or 'Tangage' to specify the axis on which we focus.
    alpha : real, optional
            A parameter to adjust the threshold. A small alpha will yield a smaller index. By default 1.
    window_width : int, optional
            The number of successive points whose mean difference is compared to the threshold. By default 5.

    Returns
    -------            
    int
            The index of the estimated beginning of the movement.
    """
    if motion == 'Lacet':
        axis = data[0]
    elif motion == 'Tangage':
        axis = data[1]
    elif motion == 'Roulis':
        axis = data[2]
    else:
        raise ValueError('The motion argument must be one of these: "Lacet", "Roulis" or "Tangage"')
    threshold = alpha*mean_succ_diff(axis)
    i=0
    while mean_succ_diff(axis[i:i+window_width]) < threshold:
        i += 1
    return i
    
#Make an audio signal when a program is over
def audio_signal(n=4,t=1):
    """
    Makes an audio signal.
    
    Parameters
    ----------
    n : int, optional
            How many times the signal is repeated. 4 by default.
    t : int, optional
            In seconds, the sleeping time between two signals. By default 1.
            
    Notes
    -----
    Mostly used to indicate that a program has finished its running.
    """
    for i in range(n):
        time.sleep(t)
        print('\a')
     
        
def write_shape(shape, file):
    """
    Writes a shape to a file.
    
    Parameters
    ----------
    shape : geometry shape
            The shape to write.(Polygon, Point...)
    file : file
            The file where the shape will be written.
    """
    file.write(shape.wkt)
    
    
def read_shape(file):
    """
    Reads a shape from a file.
    
    Parameters
    ----------
    file : file
            The file from which to read the polygon.
            
    Returns
    -------
    geometry shape 
            The shape.
    """
    return loads(file.read())