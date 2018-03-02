import matplotlib.pyplot as plt
import shapely.geometry as geometry
from descartes import PolygonPatch
import math
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
from model import myutils
from sklearn.model_selection import train_test_split
from sklearn import metrics
import sklearn.svm as svm
import pickle
import datetime


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
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
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
    alphaA = alpha_shape(polyA, 1.0)[0]
    alphaB = alpha_shape(polyB, 1.0)[0]
    AmB = alphaA.difference(alphaB)
    BmA = alphaB.difference(alphaA)
    return AmB.area + BmA.area


def matching_grid(polygon, axis=[0,1,0,1], npts_grid=[100,20]):
    """
    Discretize a space to match a polygon.
    
    Parameters
    ----------
    polygon : Polygon
            The polygon to discretize.
    axis : list, optional
            The boundary of the space considered: [xmin,xmax,ymin,ymax]. 
            [0,1,0,1] by default.
    npts_grid : array, optional
            The number of points by side of the discretization [npts_x, npts_y].
            20 by default.
    
    Returns
    -------
    array
            For each point of the discretization, 1 if the point is in the polygon and 0 otherwise.
    """
    npts_x, npts_y = npts_grid
    grid = np.zeros(npts_x*npts_y)
    hx = (axis[1]-axis[0])/(npts_x-1)
    hy = (axis[3]-axis[2])/(npts_y-1)
    pts_grid = []
    for i in range(npts_x):
        for j in range(npts_y):
            point = (axis[0]+i*hx, axis[2]+j*hy)
            pts_grid += [point]
            pt = geometry.Point(point)
            if polygon.contains(pt):
                grid[i*npts_y+j] = 1
    return grid, pts_grid


def discrete_hull(x, y, size_grid, alpha):
    """
    Make a concave hull of a set of points and return the corresponding discretization.
    
    Parameters
    ----------
    x : array
            The x-axis coordinates of the points.
    y : array
            The y-axis coordinates of the points.
    size_grid : array
            The number of points of a side of the discretization [npts_x, npts_y].
    alpha : float
            The alpha parameter for the concave hull.
    
    Returns
    -------
    (array, array), Polygon
            The corresponding grid, its points and the hull as a polygon.
    """
    coordinates = myutils.coord2points([x, y])
    hull = alpha_shape(myutils.array2MP(coordinates), alpha = alpha)[0]
    return matching_grid(hull, axis=[0,1,0.4,0.6], npts_grid=size_grid), hull


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


def train_test_model(dataset, labels):
    """
    Train and test a model using the discretization of hulls.
    
    Parameters
    ----------
    dataset : array
            Each row is a discretization of a hull.
    labels : array_like
            Labels of data (-1 for unhealthy, 1 for healthy).
    
    Returns
    -------
    OneClassSVM, float, float
            [0]: the model
            [1]: accuracy of the model at predicting the training set
            [2]: accuracy of the model at predicting the testing set
    """
    train_data, test_data, train_target, test_target = train_test_split(dataset, 
                labels, shuffle=True, train_size = 0.8)
    model = svm.OneClassSVM(kernel='rbf', nu = len(np.where(np.array(labels)==1))/len(dataset))
    model.fit(train_data, train_target)
    
    preds_train = model.predict(train_data)
    accuracy_train = metrics.accuracy_score(train_target, preds_train)
    preds_test = model.predict(test_data)
    accuracy_test = metrics.accuracy_score(test_target, preds_test)
    
    return model, accuracy_train, accuracy_test


def create_model(array_data, type_model, bins=None, size_grid=None, alpha=None,
                 labels=None):
    """
    Generate a concave hull which is the union of all concave hulls in the training set.
    
    Parameters
    ----------
    array_data : array of floats, shape (m,3,n)
            Each element is an array of 3 arrays, each corresponding to a coordinate.
    bins : array_like
            Bins for 2D histograms, [xbins, ybins]. Ignored if type_model != 'has'.
    size_grid : int
            Number of points of a side in the discretization of the hull. 
            Ignored if type_model != 'hull'.
    alpha : float
            alpha parameter for alpha shape (concave hull)
    labels : array_like
            Labels of data (-1 for unhealthy, 1 for healthy). Ignored if 
            type_model != 'hull'.
    
    Returns
    -------
    Polygon, Polygon if type_model == 'has'
            Concave hull for both pitch and roll.
    OneClassSVM, float, float if type_model == 'hull'
            The model and its accuracies at predicting training and testing sets, 
            respectively.
    """
    if type_model == 'has':
        all_points = np.concatenate([myutils.coord2points(d) for d in array_data])
        
        threshold = len(all_points)/(bins[0]*bins[1])
        
        p, r = build_set_for_hull(all_points, bins, threshold)
        model_pitch = alpha_shape(myutils.array2MP(p), alpha=3)[0].buffer(0.005)
        model_roll = alpha_shape(myutils.array2MP(r), alpha=3)[0].buffer(0.005)
        
        return model_pitch, model_roll
    
    elif type_model == 'hull':
        #B uild dataset
        dataset = []
        alpha = 3.0
        for one_acq in array_data:
            grid_p = discrete_hull(one_acq[0], one_acq[1], size_grid, alpha)[0]
            grid_r = discrete_hull(one_acq[0], one_acq[2], size_grid, alpha)[0]
            dataset += [[grid_p[0]] + [grid_r[0]]]
        # Reshape data into the proper shape
        n = len(array_data)
        dataset = np.array(dataset).reshape(n, 2*size_grid[0]*size_grid[1])
        
        return train_test_model(dataset, labels)
    
    else:
        raise ValueError('type_model should be either "has" or "hull"')
        
        
def plot_discrete_hull(grid, grid_pts, hull):
    """
    Plot a hull and its discretization.

    Parameters
    ----------
    grid : array
            Array of 1s (within hull) and 0s (outside), the discrete hull.
    grid_pts : array
            Array of points of the grid.
    hull : Polygon
            The concave hull.
    """
    plot_polygon_MP(hull)
    x, y = [pt[0] for pt in grid_pts], [pt[1] for pt in grid_pts]
    plt.scatter(x, y)
    ind_ones = []
    for i in range(len(x)):
        if grid[i] == 1:
            ind_ones += [i]
    xd = [x[i] for i in ind_ones]
    yd = [y[i] for i in ind_ones]
    plt.scatter(xd, yd, c='r')
    

def compare_to_model(new_acq, model, size_grid, alpha):
    """
    Compare a new acquisition with the model.
    
    Parameters
    ----------
    new_acq : array_like
            Array of the 3 angles (yaw, pitch, roll). Should be normalized beforehand.
    model : OneClassSVM
            Model previously built of type OneClassSVM.
    size_grid : (int, int)
            Number of points of the discretization along x and y axes respectively.
    alpha : float
            Alpha parameter for concave hulls.
            
    Returns
    -------
    bool, (array, array), Polygon, (arrray, array), Polygon
            [0]: True if healthy, False otherwise.
            [1]: Discrete hull (0s and 1s) and corresponding points for pitch.
            [2]: Hull for pitch.
            [3]: Discrete hull (0s and 1s) and corresponding points for roll.
            [4]: Hull for roll.
    """
    grid_p, hull_p = discrete_hull(new_acq[0], new_acq[1], size_grid, alpha)
    grid_r, hull_r = discrete_hull(new_acq[0], new_acq[2], size_grid, alpha)
    dataset = [[grid_p[0]] + [grid_r[0]]]
    
    dataset = np.array(dataset).reshape(1, 2*size_grid[0]*size_grid[1])
    res = model.predict(dataset)[0]
    if res == 1:
        healthy = True
    else:
        healthy = False
        
    return healthy, grid_p, hull_p, grid_r, hull_r
    

def save_model(list_dir, directory, patho_patients):
    """
    Generate and save a model.
    
    Parameters
    ----------
    list_dir : array of str
            List of directories where to find the files used to generate the model.
    directory : str
            Path to the directory where the model must be saved.
    patho_patients : array_like
            Indices of the acquisitions in list_dir which correspond to unhealthy 
            patients.
    """
    array_data, nb_acq = myutils.fetch_from_dirs(list_dir)
    array_data = myutils.preprocess_data(array_data)
    
    labels = []
    for i in range(len(list_dir)):
        if i in patho_patients:
            labels += [-1]*nb_acq[i]
        else:
            labels += [1]*nb_acq[i]
    print(labels)
    
    # For parametrization in the future ?
    alpha = 3.0
    size_grid = [20, 20]
    
    model, acc_train, acc_test = create_model(array_data, type_model='hull', 
                                              size_grid=size_grid, alpha=alpha,
                                              labels=labels)
    
    now = datetime.datetime.now()
    file_name = directory + '/hull_' + now.strftime("%m-%d-%Y_%H%M") + '.mdlhl'
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)
    with open(file_name, 'a+') as file:    
        file.write('\n' + str(acc_train) + '\n' + str(acc_test) + '\n' +
                   str(size_grid) + '\n' + str(alpha))
    

def load_model(file_path):
    """
    Loads a model previously saved.
    
    Parameters
    ----------
    file_path : str
            Path to the file in which the model has been saved.
        
    Returns
    -------
    tuple
            The SVM model and its accuracies over training and testing datasets,
            the size of the side of the grid used for discretization and the 
            alpha parameter used.
    """
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
        data = file.readlines()
        acc_train = float(data[1])
        acc_test = float(data[2])
        size_grid = [int(data[3][1:3]), int(data[3][5:7])]
        alpha = float(data[4])
    return model, acc_train, acc_test, size_grid, alpha


if __name__ == '__main__':
    """ direct = ['data/guillaume2/', 'data/tests/']
    ind = [1]
    save_model(direct, '.', patho_patients=ind)
    """
    x = load_model('hull_03-01-2018_1301.mdlhl')