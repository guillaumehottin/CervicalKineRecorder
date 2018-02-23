import hulls
import splines
import datetime
from shapely.wkt import loads
import matplotlib.pyplot as plt
import myutils
import numpy as np


def check_healthy(score_spline, score_hull, hull_threshold, spline_threshold):
    """
    Checks whether a new piece of data matches the model.
    
    Parameters
    ----------
    score_hull : int
            Number of points out of the model hull.
    score_spline : real
            Standard deviation of the distance to the model spline.
    hull_threshold : int
            Number of points outside the hull from which the data is deemed 
            unmatching.
    spline_threshold : real
            Threshold to compare the score of the new_data against the spline.
            
    Returns
    -------
    bool
            True if the patient is healthy, False otherwise.
    """
    if score_spline > spline_threshold:
        return False
    if score_hull > hull_threshold:
        return False
    return True


def plot_spline_curve(curve, spline):
    """
    Plot the curve of the acquisition and the spline.
    
    Parameters
    ----------
    curve : array of arrays
            First array is x-axis component of the acquisition, second is y-axis.
    spline : array of array
            Same as curve but for the spline.
    """
    plt.figure()
    plt.plot(curve[0], curve[1])
    plt.plot(spline[0], spline[1])
    plt.show()
    
    
def plot_hull_curve(curve, hull):
    """
    Plot the curve of the acquisition and the hull.
    
    Parameters
    ----------
    curve : array of arrays
            First array is x-axis component of the acquisition, second is y-axis.
    hull : Polygon
            Model hull.
    """
    plt.figure()
    hulls.plot_polygon_MP(hull)
    plt.plot(curve[0], curve[1])
    plt.show()

    
def save_model(array_data, directory):
    """
    Generate and save a model.
    
    Parameters
    ----------
    array_data : array of arrays of points
            Each element is an array of points.
    directory : str
            Path to the directory where the model must be saved.
    """
    hull_model = hulls.create_model(array_data)
    spline_model = splines.create_model(array_data)
    now = datetime.datetime.now()
    file_name = directory + '/spline_hull_' + now.strftime("%m-%d-%Y_%H%M") + '.mdl'
    with open(file_name, 'w+') as file:
        file.write(hull_model.wkt + '\n' + spline_model)
        
    
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
            First element is the hull model (a Polygon), second is the spline.
    """
    with open(file_path, 'r+') as file:
        data = file.readlines()
        hull = loads(data[0][:-2])
        spline = []
    #spline = data[1]
    return hull, spline


if __name__ == '__main__':
    direct = 'data/guillaume2/'
    list_files = myutils.fetch_files(dir_name=direct,sub_dir='Normalized',extension='.orpl')
    yaw_pitch = [myutils.get_coord(f)[0:2] for f in list_files]
    yaw_roll = [myutils.get_coord(f)[0:3:2] for f in list_files]
    list_all_points_pitch = np.array(yaw_pitch)
    list_all_points_roll= np.array(yaw_roll)
    hull_pitch = hulls.create_model([myutils.coord2points(coord) for coord in list_all_points_pitch])
    hull_roll = hulls.create_model([myutils.coord2points(coord) for coord in list_all_points_roll])
    angle_x,angle_y,xsp,ysp = splines.interpolate_spline(list_all_points_pitch[0], 150)
    angle_x,angle_y,xsr,ysr = splines.interpolate_spline(list_all_points_roll[0], 150)
    plot_spline_curve(yaw_pitch[0], (xsp, ysp))
    plot_spline_curve(yaw_roll[0], (xsr, ysr))