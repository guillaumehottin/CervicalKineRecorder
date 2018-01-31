import matplotlib.pyplot as plt
import shapely.geometry as geometry
from descartes import PolygonPatch
import math
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import myutils

def plot_polygon_MP(polygon):
    """
    Plot a polygon using PolygonPatch.
    @param polygon: MultiPoint, the polygon to plot
    """
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    margin = .3
    x_min, y_min, x_max, y_max = polygon.bounds
    ax.set_xlim([x_min-margin, x_max+margin])
    ax.set_ylim([y_min-margin, y_max+margin])
    patch = PolygonPatch(polygon, fc='#999999',
                         ec='#000000', fill=True,
                         zorder=-1)
    ax.add_patch(patch)
    return fig

def plot_many_polygons(lst_poly):
    x_max = 0
    y_max = 0
    x_min = 0
    y_min = 0
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    margin = .3
    for poly in lst_poly:
        x_min_curr, y_min_curr, x_max_curr, y_max_curr = poly.bounds
        if x_max < x_max_curr:
            x_max = x_max_curr
        if y_max < y_max_curr:
            y_max = y_max_curr
        if y_min > y_min_curr:
            y_min = y_min_curr
        if x_min > x_min_curr:
            x_min = x_min_curr
        color = myutils.RGBA_arg()
        patch = PolygonPatch(poly, fc=color,
                         ec=color, fill=True,
                         zorder=-1)
        ax.add_patch(patch)
    ax.set_xlim([x_min-margin, x_max+margin])
    ax.set_ylim([y_min-margin, y_max+margin])
    ax.legend([str(i+1) for i in range(len(lst_poly))])
    return fig

#Convex hull
def plot_convex_hull(pts):
    """
    Plot a convex hull with an array of points as input.
    """
    point_collection = myutils.array2MP(pts)
    plt.figure(figsize=(10,10))
    fig = plot_polygon_MP(point_collection.convex_hull)
    plt.plot(x,y,'o')
    return fig

###############################################
#Concave hull

def add_edge(edges, edge_points, coords, i, j):
    """ 
    Add a line between the ith and jth points, if not in the list already.
    """
    if not (i,j) in edges and not (j,i) in edges:
        edges.add((i,j))
        edge_points.append(coords[[i,j]])

def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
		  
    coords = np.array([point.coords[0] for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points

#Distance for clustering
def hull_distance(polyA,polyB):
    alphaA,_ = alpha_shape(polyA,0.2)
    alphaB,_ = alpha_shape(polyB,0.2)
    AmB = alphaA.difference(alphaB)
    BmA = alphaB.difference(alphaA)
    return AmB.area + BmA.area


#############################################################
"""
c = [[0,0],[3,7],[-3,4],[-6,-4],[4,-7],[-4,-8]]
r = [4,4,3,3,5,2]
c2 = [[1,2],[-3,-4],[2,3]]
r2 = [2,5,5]
n = 100

x,y,pts = myutils.generate_clusters(c,r,n)
x2,y2,pts2 = myutils.generate_clusters(c2,r2,n)

polys = myutils.generate_MP(12,cl_max=1,alpha=0.5)

plot_many_polygons([alpha_shape(p,alpha=0.6)[0] for p in polys])
f = fclusterdata(np.arange(len(polys)).reshape((len(polys),1)),1.0,metric=hull_dist_indices)
print(f)
"""

"""
from scipy.cluster.hierarchy import fclusterdata

files = myutils.fetch_files(dir_name='bonnes_mesures',sub_dir='Normalized')
points_collection = []
for file in files:
    yaw,pitch,roll = myutils.get_coord(file)
    coordinates = myutils.coord2points([pitch,yaw])
    points_collection += [myutils.array2MP(coordinates)]
    
def hull_dist_indices(first,second):
    return hull_distance(points_collection[int(first[0])],points_collection[int(second[0])])

n = len(points_collection)
threshold = [1.05]
f = []
for i in threshold:
    f += [fclusterdata(np.arange(n).reshape((n,1)),i,metric=hull_dist_indices)]
for x in f:
    print(x)
"""

yaw,pitch,roll = myutils.get_coord('bonnes_mesures\\bonnemaison_elodie_22\\Normalized\\Fri Dec  8 15_10_38 2017 - Lacet.orpl')
yaw_pitch = myutils.coord2points([yaw,pitch])
plot_polygon_MP(alpha_shape(myutils.array2MP(yaw_pitch),alpha=1)[0])
plt.plot(yaw,pitch)
 
"""
alpha=0.2
t=0.5
[28  1  1 25 40 41  9  4 29  2 20 27 35  3  2 36 38 30 13 15 12 20 33  6  5
 11 24 17 29 13 31  3 22 10  7 34 19 18 23 42 26 37 21 18 16 11  6  5 32 14
  4  8 39]
t=1.0
[16  1  1 13 26 27  7  4 17  2  9 15 21  3  2 22 24 17  9  9  9  9 19  6  5
  9 12  9 17  9 17  3 10  8  6 20  9  9 11 28 14 23  9  9  9  9  6  5 18  9
  4  6 25]
t=1.05
[16  1  1 13 26 27  7  4 17  2  9 15 21  3  2 22 24 17  9  9  9  9 19  6  5
  9 12  9 17  9 17  3 10  8  6 20  9  9 11 28 14 23  9  9  9  9  6  5 18  9
  4  6 25]
t=1.5
[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
t=2.0
[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]

alpha=0.4 (pas norm)
t=1.0
[20  1  1  5 25 23 21 26  6  6  6  6 18  6  6  6 15 19 17  2 10  6  3  8  3
  9  2  6 16  6 13  6  6 12  6  6  4  4  6 14 22 11 24  5  6  6  6  6  6  6
  6  6  7]
t=0.1
[36  1  1  5 41 39 37 42 10 17 13 11 34 17  9  8 31 35 33  2 26 21  3 24  3
 25  2 18 32  9 29  8 14 28 19 22  4  4 12 30 38 27 40  5 11 15  6  7 20 14
 16  6 23]

alpha=0.6
t=0.01
[31  1  1 27 38 37  7 13  3 26 29 35  4 19 23  2  2 32 20 21 17 18  6  6  8
 16 30 28  3 20 15 22 27 12  9 34  4  5 25 15 31 14 33 13 22 16  8 11 14 19
 24 10 36]
t=0.1
[31  1  1 27 38 37  7 13  3 26 29 35  4 19 23  2  2 32 20 21 17 18  6  6  8
 16 30 28  3 20 15 22 27 12  9 34  4  5 25 15 31 14 33 13 22 16  8 11 14 19
 24 10 36]
t=1.0
[19  1  1 16 25 24  5  6  3 15 17 22  4 10 12  2  2 19 10 10  9  9  5  5  5
  9 18 16  3 10  8 11 16  5  5 21  4  4 14  8 19  7 20  6 11  9  5  5  7 10
 13  5 23]
t=2.0
[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]

alpha=0.8
t=0.1 idem 0.5
[30  3  3  6 39 35 15 25 36  2 40 38 18  1  1  5 38  4 20 22 21 27  7  7  8
 29 20  6  4 26 32 14 13 16  9 33 12 17  5 19 19 37 31 28 13 24  8 11 23 26
 21 10 34]
t=1.0
[ 8  2  2  5 17 13  5  7 14  1 18 16  5  1  1  4 16  3  7  7  7  7  5  5  5
  7  7  5  3  7 10  5  5  5  5 11  5  5  4  6  6 15  9  7  5  7  5  5  7  7
  7  5 12]
"""

"""
concave_hull, edge_points = alpha_shape(myutils.array2MP(pts),alpha=0.7)
plot_polygon_MP(concave_hull.buffer(1,resolution=1))
plt.plot(x,y,'o', color='#f16824')
"""
