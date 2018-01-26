import matplotlib.pyplot as plt
import shapely.geometry as geometry
from descartes import PolygonPatch
import math
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import myutils

#Convex hull
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

def plot_polygon_lst(pts):
    """
    Plot a polygon with an array of points as input.
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

#############################################################
c = [[0,0],[3,7],[-3,4],[-6,-4],[4,-7],[-4,-8]]
r = [4,4,3,3,5,2]
n = 100

x,y,pts = myutils.generate_clusters(c,r,n)
concave_hull, edge_points = alpha_shape(myutils.array2MP(pts),alpha=0.7)
plot_polygon_MP(concave_hull.buffer(1,resolution=1))
plt.plot(x,y,'o', color='#f16824')

