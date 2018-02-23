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

    
def save_model(list_dir, directory):
    """
    Generate and save a model.
    
    Parameters
    ----------
    list_dir : array of str
            List of directories where to find the files used to generate the model.
    directory : str
            Path to the directory where the model must be saved.
    """
    array_data = myutils.fetch_from_dirs(list_dir)
    hull_model_p, hull_model_r = hulls.create_model(array_data)
    spline_pitch, spline_roll = splines.create_model(array_data)
    now = datetime.datetime.now()
    file_name = directory + '/has_' + now.strftime("%m-%d-%Y_%H%M") + '.mlhas'
    with open(file_name, 'w+') as file:
        file.write(hull_model_p.wkt + '\n' + hull_model_r.wkt + '\n' + str(spline_pitch) + '\n' + str(spline_roll))
        
    
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
        hull_pitch = loads(data[0])
        hull_roll = loads(data[1])
        spline_std_pitch = float(data[2])
        spline_std_roll = float(data[3])
    #spline = data[1]
    return hull_pitch, hull_roll, spline_std_pitch, spline_std_roll


if __name__ == '__main__':
    direct = 'data/guillaume2/Normalized'
    #save_model([direct], '.')
        load_model("has_02-23-2018_1808.mlhas")