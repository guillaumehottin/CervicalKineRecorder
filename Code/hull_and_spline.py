import hulls
import splines
import datetime
from shapely.wkt import loads

def check_new_data(model_hull, new_data, hull_threshold, spline_threshold):
    """
    Checks whether a new piece of data matches the model.
    
    Parameters
    ----------
    model_hull : Polygon
            Hull representing the boundaries whithin which the new points
            must be.
    model_spline : array
            Mean spline with which to compare the new data.
    new_data : array
            Array of points representing the new data.
    hull_threshold : int
            Number of points outside the hull from which the data is deemed 
            unmatching.
    spline_threshold : real
            Threshold to compare the score of the new_data against the spline.
            
    Returns
    -------
    bool
            True if the new data matches the model.
    """
    if splines.score_model(new_data, 300) > spline_threshold:
        return False
    if hulls.score_model(model_hull, new_data) > hull_threshold:
        return False
    return True


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


