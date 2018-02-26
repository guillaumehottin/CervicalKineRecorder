import hulls
import splines
import datetime
from shapely.wkt import loads
import matplotlib.pyplot as plt
import myutils
import time


def compare_to_model(new_acq, model):
    """
    Compare a new acquisition with the model.
    
    Parameters
    ----------
    new_acq : array_like
            Array of the 3 angles (yaw, pitch, roll). Should be normalized beforehand.
    model : tuple
            Model previously built: (hull_pitch, hull_roll, spline_threshold_pitch,
            spline_threshol_roll).
            
    Returns
    -------
    bool, int, int, float, float
            [0]: True if healthy, False otherwise.
            [1], [2]: Number of points out of the hull for pitch and roll respectively.
            [3], [4]: Deviation from the threshold for pitch and roll respectively.
    """
    hull_pitch, hull_roll, spline_threshold_pitch, spline_threshold_roll = model
    new_pts_pitch = myutils.coord2points(new_acq[0:2])
    new_pts_roll= myutils.coord2points(new_acq[0:3:2])
    
    npts = len(new_pts_pitch)
    rate_out_pitch = hulls.pts_out_poly(hull_pitch, new_pts_pitch)/npts
    rate_out_roll = hulls.pts_out_poly(hull_roll, new_pts_roll)/npts
    
    xs_pitch, ys_pitch, ind_pitch = splines.interpolate_spline(new_acq[0:2])
    xs_roll, ys_roll, ind_roll = splines.interpolate_spline(new_acq[0:3:2])
    score_pitch = splines.score_model(new_acq[0:2], xs_pitch, ys_pitch, ind_pitch)
    score_roll = splines.score_model(new_acq[0:3:2], xs_roll, ys_roll, ind_roll)
    err_spline_pitch = spline_threshold_pitch - score_pitch
    err_spline_roll = spline_threshold_roll - score_roll
    
    healthy = True
    if (rate_out_pitch > 0.1 or rate_out_pitch > 0.1 or err_spline_pitch < 0 or
            err_spline_roll < 0):
        healthy = False
    return healthy, rate_out_pitch, rate_out_roll, err_spline_pitch, err_spline_roll


def plot_spline_curve(spline, curve):
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
    
    
def plot_hull_curve(hull, curve):
    """
    Plot the curve of the acquisition and the hull.
    
    Parameters
    ----------
    curve : array of arrays
            First array is x-axis component of the acquisition, second is y-axis.
    hull : Polygon
            Model hull.
    """
    hulls.plot_polygon_MP(hull)
    plt.plot(curve[0], curve[1])
    plt.show()


def preprocess_data(array_data, type_norm = 'global'):
    """
    Normalize data for all acquisitions of a list.
    
    Parameters
    ----------
    array_data : list
            List of lists of coordinates.
    type_norm : str
            Type of normalization (see normalize function in myutils).
            
    Returns
    -------
    list
         Normalized data.
    """
    norm_array = []
    for one_acq in array_data:
        norm_array.append(myutils.normalize(one_acq[0], one_acq[1], one_acq[2], type_norm))
    return norm_array

    
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
    bins = [50, 20]
    array_data = preprocess_data(array_data)
    hull_model_p, hull_model_r = hulls.create_model(array_data, bins)
    spline_pitch, spline_roll = splines.create_model(array_data)
    
    now = datetime.datetime.now()
    file_name = directory + '/has_' + now.strftime("%m-%d-%Y_%H%M") + '.mdlhs'
    with open(file_name, 'w+') as file:
        file.write(hull_model_p.wkt + '\n' + hull_model_r.wkt + '\n' 
                   + str(spline_pitch) + '\n' + str(spline_roll))
    
    return hull_model_p, hull_model_r
    

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
            First two elements are the hull models (Polygons), next two are the 
            splines mean standard deviations.
    """
    with open(file_path, 'r+') as file:
        data = file.readlines()
        if len(data) != 4:
            raise ValueError('The file does not have the coorect structure '
                             + '(number of lines different from 4)')
        hull_pitch = loads(data[0])
        hull_roll = loads(data[1])
        spline_std_pitch = float(data[2])
        spline_std_roll = float(data[3])
    return hull_pitch, hull_roll, spline_std_pitch, spline_std_roll


if __name__ == '__main__':
    direct = ['data/guillaume2/']
    
    """
    start = time.process_time()
    hullp, hullr  = save_model(direct, '.')
    elapsed = time.process_time()-start
    print("Time elapsed: {0}".format(elapsed))
    """
    model = load_model("has_02-26-2018_1154.mdlhs")
    acq = preprocess_data([myutils.get_coord('data/tests/2018_02_21_13_48_59_.orpl')])[0]
    print(compare_to_model(acq, model))
