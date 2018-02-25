import matplotlib.pyplot as plt
import shapely.geometry as geometry
from descartes import PolygonPatch
import math
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import myutils

from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull


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
    
    Parameters
    ----------
    points : Iterable container of points.
    alpha : real
            alpha value to influence the gooeyness of the border. Smaller numbers
            don't fall inward as much as larger numbers.
            Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
		  
    coords = np.array([point.coords[0] for point in points])
    tri = Delaunay(coords)
    print("Delaunay done...")
    print(str(len(tri.vertices))+" vertices")
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
    print("Triangles polygonized")
    return cascaded_union(triangles), edge_points


def hull_distance(polyA, polyB):
    """
    Distance between two hulls, defined by the sum of their differences areas.
    
    polyA : MultiPoint
            First set of points
    polyB : MultiPoint 
            Second set of points
    """
    alphaA,_ = alpha_shape(polyA,1.0)
    alphaB,_ = alpha_shape(polyB,1.0)
    AmB = alphaA.difference(alphaB)
    BmA = alphaB.difference(alphaA)
    return AmB.area + BmA.area


def matching_grid(polygon, axis=[0,1], npts=20):
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


def in_cvx_hull3(hull, pt):
    """
    Check whether pt is in hull (3D). (Not always working!)
    
    Parameters
    ----------
    hull : ConvexHull
            3D points defining the hull
    pt : array
            The point
    
    Returns
    -------
    bool
            True if pt is in hull.
    """
    new_hull = ConvexHull(np.concatenate((hull.points, [pt])))
    return np.array_equal(new_hull.vertices, hull.vertices)


def pts_out_hull3(hull, pts):
    """
    Number of points of pts which are in hull (3D). (Not always working!)
    
    Parameters
    ----------
    hull : ConvexHull
            3D points defining the hull
    pts : array
            The set of points
    
    Returns
    -------
    int
            Number of points in hull
    array
            Coordinates of the points not in hull
    """
    
    """
    n = 0
    x = []
    for pt in pts:
        if not in_cvx_hull3(hull, pt):
            n += 1
            x.append(pt)
    return n, x
    """
    
    if not isinstance(hull.points,Delaunay):
        hull = Delaunay(hull.points)

    x = hull.find_simplex(pts)<0
    indices_out = np.where(x)[0]
    n = len(indices_out)
    return n, indices_out


def points_in_area(x_coords, y_coords, xlims, ylims):
    """
    Get the points that are in a delimited area.
    
    Parameters
    ----------
    x_coords : array_like
            X-axis coordinates.
    y_coords : array_like
            Y-axis coordinates.
    xlims : array_like
            The area limits for the x-axis, [x_low, x_up]
    ylims : array_like
            The area limits for the y-axis, [y_low, y_up]
    """
    pts = []
    x_low, x_up = xlims
    y_low, y_up = ylims
    for i in range(len(x_coords)):
        x, y = x_coords[i], y_coords[i]
        if x >= x_low and x < x_up and y >= y_low and y < y_up:
            pts += [[x, y]]
    return pts
            

def build_set_for_hull(array_data, bins, threshold):
    """
    Build the set of points that will be kept to make the hull (i.e., we do not 
    consider points in areas whose density is too low).
    
    Parameters
    ----------
    array_data : array_like
            Contains three arrays of floats, for each angle (yaw, pitch ,roll) respectively.
    bins : array_like
            Bins for the 2D histograms, in the shape [xbins, ybins].
    threshold : int
            Minimum number of points in an area for which we keep the area.
            
    Returns
    -------
    tuple of 2 arrays
            The first array is the points kept for pitch=f(yaw), the second
            for roll=f(yaw).
    """
    #Build 2D histograms
    yaw = [x[0] for x in array_data]
    pitch = [x[1] for x in array_data]
    roll = [x[2] for x in array_data]
    print('Total of points = '+str(len(yaw)))
    hp, xedge, yedge = np.histogram2d(yaw, pitch, bins=bins, range=[[0,1],[0.43,0.57]])
    hr, _, _ = np.histogram2d(yaw, roll, bins=bins, range=[[0,1],[0.43,0.57]])
    
    #Determine points to be kept
    pts_pitch = []
    pts_roll = []
    for j in range(bins[1]):
        for i in range(bins[0]):
            #Keep areas that contain enough points
            xlims = xedge[i:i+2]
            ylims = yedge[j:j+2]
            if hp[i, j] >= threshold:
                pts_pitch += points_in_area(yaw, pitch, xlims, ylims)
            if hr[i, j] >= threshold:
                pts_roll += points_in_area(yaw, roll, xlims, ylims)
    return pts_pitch, pts_roll


def create_model(array_data):
    """
    Generate a concave hull which is the union of all concave hulls in the training set.
    
    Parameters
    ----------
    array_data : array of arrays of arrays of floats
            Each element is an array of 3 arrays, each corresponding to a coordinate.
            
    Returns
    -------
    tuple of Polygon
            Concave hull for both pitch and roll.
    """
    
    """
    array_data = [myutils.coord2points(d) for d in array_data]
    first_acq = array_data.pop(0)
    
    bins = [10, 5]
    threshold = 10
    #p = [x[0:2] for x in first_acq]
    #r = [x[0:3:2] for x in first_acq]
    
    p, r = build_set_for_hull(first_acq, bins, threshold)
    model_pitch = alpha_shape(myutils.array2MP(p), alpha=3)[0]
    model_roll = alpha_shape(myutils.array2MP(r), alpha=3)[0]
    for one_acq in array_data:
        p, r = build_set_for_hull(one_acq, bins, threshold)
        #p = [x[0:2] for x in first_acq]
        #r = [x[0:3:2] for x in first_acq]
    
        hull_pitch = alpha_shape(myutils.array2MP(p), alpha=3)[0]
        hull_roll = alpha_shape(myutils.array2MP(r), alpha=3)[0]
        model_pitch = model_pitch.union(hull_pitch)
        model_roll = model_roll.union(hull_roll)
    return model_pitch, model_roll
    """
    
    all_points = np.concatenate([myutils.coord2points(d) for d in array_data])
    
    bins = [50, 20]
    threshold = len(all_points)/(bins[0]*bins[1])
    
    p, r = build_set_for_hull(all_points, bins, threshold)
    print("Point set built...")
    print(str(len(p))+" points in pitch")
    print(str(len(r))+" points in roll")
    model_pitch = alpha_shape(myutils.array2MP(p), alpha=3)[0].buffer(0.005)
    print("Pitch model built...")
    model_roll = alpha_shape(myutils.array2MP(r), alpha=3)[0].buffer(0.005)
    print("Roll model built...\nBoth models built...")
    
    plot_polygon_MP(model_pitch)
    plt.scatter([x[0] for x in p], [x[1] for x in p])
    plot_polygon_MP(model_roll)
    plt.scatter([x[0] for x in r], [x[1] for x in r])
    return model_pitch, model_roll

#############################################################

if __name__ == '__main__':
   
    yaw,pitch,roll = myutils.get_coord('bonnes_mesures/bonnemaison_elodie_22/Normalized/Fri Dec  8 15_10_38 2017 - Lacet.orpl')
    yaw_pitch = myutils.coord2points([yaw,pitch])
    hull = alpha_shape(myutils.array2MP(yaw_pitch),alpha=3)[0].buffer(0.05)
    plot_polygon_MP(hull)
    plt.plot(yaw,pitch)
    print(matching_grid(hull))
    
    
    """
    pts = np.array(myutils.coord2points([yaw,pitch,roll]))
    
    hull = ConvexHull(pts)

    n, notl = pts_out_hull3(hull, pts)
    
    #l = [np.where(pts == y)[0][0] for y in x]
    l = [k for k in range(len(pts)) if k not in notl]
    
    fig = plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.scatter(yaw[l], pitch[l], roll[l])
    
    x = yaw[notl]
    y = pitch[notl]
    z = roll[notl]
    
    ax.scatter(x,y,z,'r')
    plt.show()
"""