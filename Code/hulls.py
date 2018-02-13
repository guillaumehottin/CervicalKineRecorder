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
    
    Parameters
    ----------
    polygon : MultiPoint
            The polygon to plot
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
    """
    Plot a list of polygons contained in a list.
    
    Parameters
    ----------
    lst_poly : array(MultiPoints)
            List of polygons
            
    Returns
    -------
    figure
            The corresponding figure.
    """
    x_max = 0
    y_max = 0
    x_min = 0
    y_min = 0
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    margin = .3
    for poly in lst_poly:
        #Determine the axes limits
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
    Plot a convex hull.
    
    Parameters
    ----------
    pts : array(Point)
            The points whose the convex hull is expected.
            
    Returns
    -------
    figure
            The corresponding figure.
    """
    point_collection = myutils.array2MP(pts)
    plt.figure(figsize=(10,10))
    fig = plot_polygon_MP(point_collection.convex_hull)
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


def hull_distance(polyA,polyB):
    """
    Distance between two hulls, defined by the sum of their differences areas.
    @param polyA (MultiPoint): first set of points
    @param polyA (MultiPoint): first set of points
    """
    alphaA,_ = alpha_shape(polyA,1.0)
    alphaB,_ = alpha_shape(polyB,1.0)
    AmB = alphaA.difference(alphaB)
    BmA = alphaB.difference(alphaA)
    return AmB.area + BmA.area


def matching_grid(polygon,axis=[0,1],npts=20):
    """
    Discretize a space to match a polygon.
    
    Parameters
    ----------
    polygon : Polygon
            The polygon to discretize.
    axis : list, optional
            The min and the max of the square space. [0,1] by default.
    npts : int, optional
            The number of points by side of the discretization. 20 by default.
    
    Returns
    -------
    array
            For each point of the discretization, 1 if the point is in the polygon and 0 otherwise.
    """
    grid = np.zeros(npts**2)
    h = (axis[1]-axis[0])/(npts-1)
    for i in range(npts):
        for j in range(npts):
            pt = geometry.Point(i*h,j*h)
            if polygon.contains(pt):
                grid[i*npts+j] = 1
    return grid       


def hull_grid(x, y, m, alpha, buff_size):
    """
    Make a concave hull of a set of points and return the corresponding discretization.
    
    Parameters
    ----------
    x : array
            The x-axis coordinates of the points.
    y : array
            The y-axis coordinates of the points.
    m : int
            The number of points of a side of the discretization.
    alpha : real
            The alpha parameter for the concave hull.
    buff_size : real
            The buffer size of the concave hull, i.e. a margin.
    
    Returns
    -------
    array
            The corresponding grid.
    """
    coordinates = myutils.coord2points([x, y])
    hull = alpha_shape(myutils.array2MP(coordinates), alpha = alpha)[0].buffer(buff_size)
    return matching_grid(hull, npts = m)


def pts_out_poly(poly, pts):
    """
    The number of points belonging to a set of points which are not within a polygon frame.
    
    Parameters
    ----------
    poly : Polygon
            The polygon.
    pts : array
            Array of points.
            
    Returns
    -------
    int
            The number of points outside the polygon.
    """
    n = 0
    for pt in pts:
        
        if not poly.contains(pt):
            n += 1
    return n


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

concave_hull, edge_points = alpha_shape(myutils.array2MP(pts),alpha=0.7)
plot_polygon_MP(concave_hull.buffer(1,resolution=1))
plt.plot(x,y,'o', color='#f16824')
"""


yaw,pitch,roll = myutils.get_coord('bonnes_mesures/bonnemaison_elodie_22/Normalized/Fri Dec  8 15_10_38 2017 - Lacet.orpl')
yaw_pitch = myutils.coord2points([yaw,pitch])
hull = alpha_shape(myutils.array2MP(yaw_pitch),alpha=3)[0].buffer(0.05)
plot_polygon_MP(hull)
plt.plot(yaw,pitch)
print(matching_grid(hull))

