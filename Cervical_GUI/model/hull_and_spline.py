from model import splines, hulls
import datetime
from shapely.wkt import loads
import matplotlib.pyplot as plt
from model import myutils


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
    rate_out_pitch = hulls.pts_out_poly(hull_pitch, new_pts_pitch) / npts
    rate_out_roll = hulls.pts_out_poly(hull_roll, new_pts_roll) / npts
    
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
    res_comparison = {'healthy': healthy, 'rate_out_pitch': rate_out_pitch, 
               'rate_out_roll': rate_out_roll, 'err_spline_pitch': err_spline_pitch, 
               'err_spline_roll': err_spline_roll}
    to_plot_pitch = {'hull': hull_pitch, 'xs': xs_pitch, 'ys': ys_pitch,
                     'curve': new_acq[0:2], 'type_motion': 'pitch'}
    to_plot_roll = {'hull': hull_roll, 'xs': xs_roll, 'ys': ys_roll,
                     'curve': new_acq[0:3:2], 'type_motion': 'roll'}
    return res_comparison, to_plot_pitch, to_plot_roll
    
    
def plot_hull_spline(hull, spline, curve, type_motion):
    """
    Plot the curve of the acquisition and the hull.
    
    Parameters
    ----------
    curve : array of arrays
            First array is x-axis component of the acquisition, second is y-axis.
    hull : Polygon
            Model hull.
    spline : array of array
            Same as curve but for the spline.
    type_motion : str
            'pitch' or 'roll', according to the angle considered.
    """
    hulls.plot_polygon_MP(hull)
    plt.plot(curve[0], curve[1], 'b--')
    plt.plot(spline[0], spline[1], 'r')
    if type_motion == 'pitch':
        plt.ylim([0.44, 0.56])
    elif type_motion == 'roll':
        plt.ylim([0.32, 0.67])
    else:
        raise ValueError('type_motion must be either "pitch" or "roll"')
    plt.ylabel(type_motion)
    plt.xlim([-0.05, 1.05])
    plt.xlabel('yaw')
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
    array_data = myutils.fetch_from_dirs(list_dir)[0]
    bins = [50, 20]
    array_data = myutils.preprocess_data(array_data)
    hull_model_p, hull_model_r = hulls.create_model(array_data, type_model='has', bins=bins)
    spline_pitch, spline_roll = splines.create_model(array_data)
    
    now = datetime.datetime.now()
    file_name = directory + '/has_' + now.strftime("%m-%d-%Y_%H%M") + '.mdlhs'
    with open(file_name, 'w+') as file:
        file.write(hull_model_p.wkt + '\n' + hull_model_r.wkt + '\n' 
                   + str(spline_pitch) + '\n' + str(spline_roll))
    

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
            raise ValueError('The file does not have the correct structure '
                             + '(number of lines different from 4)')
        hull_pitch = loads(data[0])
        hull_roll = loads(data[1])
        spline_std_pitch = float(data[2])
        spline_std_roll = float(data[3])
    return hull_pitch, hull_roll, spline_std_pitch, spline_std_roll


if __name__ == '__main__':
    direct = ['data/guillaume2/']
    save_model(direct, '.')

    """
    model = load_model("has_02-26-2018_1154.mdlhs")
    acq = myutils.preprocess_data([myutils.get_coord('data/guillaume2/patho4.orpl')])[0]
    print(compare_to_model(acq, model))
    """