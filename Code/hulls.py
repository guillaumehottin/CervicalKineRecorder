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
    
    Returns
    -------
    Polygon
            The concave hull.
    list
            Edge points of the concave hull.
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
    
    Parameters
    ----------
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
            Array of points coordinates.
            
    Returns
    -------
    int
            The number of points outside the polygon.
    """
    n = 0
    for pt in pts:
        point = geometry.asPoint(pt)
        if not poly.contains(point):
            n += 1
    return n


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


def create_model(array_data, bins):
    """
    Generate a concave hull which is the union of all concave hulls in the training set.
    
    Parameters
    ----------
    array_data : array of arrays of arrays of floats
            Each element is an array of 3 arrays, each corresponding to a coordinate.
    bins : array_like
            Bins for 2D histograms, [xbins, ybins]
    
    Returns
    -------
    tuple of Polygon
            Concave hull for both pitch and roll.
    """    
    all_points = np.concatenate([myutils.coord2points(d) for d in array_data])
    
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


if __name__ == '__main__':
    yaw,pitch,roll = myutils.get_coord('bonnes_mesures/bonnemaison_elodie_22/Normalized/Fri Dec  8 15_10_38 2017 - Lacet.orpl')
    yaw_pitch = myutils.coord2points([yaw,pitch])
    hull = alpha_shape(myutils.array2MP(yaw_pitch),alpha=3)[0].buffer(0.05)
    plot_polygon_MP(hull)
    plt.plot(yaw,pitch)
    print(matching_grid(hull))
    