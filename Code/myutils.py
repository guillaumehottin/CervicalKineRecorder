import random as rd
import shutil
import shapely.geometry as geometry
import numpy as np
import os

#Generate clusters based on their center and radius
def generate_clusters(centers,radii,npts_by_clusters):
    pts = []
    x = []
    y = []
    for j in range(len(radii)):
        xj = centers[j][0]
        yj = centers[j][1]
        rj = radii[j]
        for i in range(npts_by_clusters):
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

#Define RGBA color
def RGBA_arg():
    hex_str = hex(int(rd.random()*16777215))[2:]
    n = len(hex_str)
    while n < 6:
        hex_str = '0'+hex_str
        n = len(hex_str)
    return '#'+hex_str
    
#To fetch files in a specified folder and its sub folders, returns the list of the paths to theses files
def fetch_files(dir_name='.',extension='.orpl',sub_dir=''):
    res = []
    list_dir = next(os.walk(dir_name))[1]
    for folder in list_dir:
        if sub_dir == '':
            path = dir_name+'/'+folder
        else:
            path = dir_name+'/'+folder+'/'+sub_dir
        for file in os.listdir(path):
            if extension in file:
                res += [path+'/'+file] 
    return res

#Get list of coordinates in an ORPL file (yaw,pitch_roll)
def get_coord(file_path):
    f = open(file_path,"r")
    data = f.readlines()
    f.close()
    yaw_l, pitch_l, roll_l = [],[],[]

    data.pop(0)
    for i in range(len(data)):
        elems = data[i].split(" ")
        yaw_l.append(elems[0])
        pitch_l.append(elems[1])
        roll_l.append(elems[2])

    pitch_l = list(map(float, pitch_l))
    yaw_l = list(map(float, yaw_l))
    roll_l = list(map(float, roll_l))

    return (pitch_l,yaw_l,roll_l)

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

#Return the mean difference between 2 successive elements in an array
def mean_succ_diff(data):
    n = len(data)
    s=0
    for i in range(n-1):
        s += abs(data[i]-data[i+1])
    return s/(n-1)

#Detect when the patient starts to move
#data = yaw,pitch,roll
def start_movement_index(data,motion,alpha=1,window_width=5):
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
    