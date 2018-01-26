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