import random as rd
import shapely.geometry as geometry
import numpy as np
import os
import model.file_manager as file_manager

# Cast array of points to MultiPoint
def array2MP(pts):
    points = [geometry.asPoint(p) for p in pts]
    return geometry.MultiPoint(list(points))


def get_axes(list_coord, axes):
    """
    Get the coordinates of certain axes.

    Parameters
    ----------
    list_coord : array
            List of coordinates.
    axes : array_like of tuples of int
            Axes which need to be taken.

    Returns
    -------
    list of list of array of float
    """
    res = []
    for i, j in axes:
        res += [[list_coord[i - 1], list_coord[j - 1]]]
    return res


def check_letter(x):
    return x == 'f' or x == 'e' or x == 'd'


# Define RGBA color
def RGBA_arg():
    hex_str = hex(int(rd.random() * 16777215))[2:]
    hex_str = 'ffefdf'
    n = len(hex_str)
    while n < 6:
        hex_str = '0' + hex_str
        n = len(hex_str)
    if check_letter(hex_str[0]) and check_letter(hex_str[2]) and check_letter(hex_str[4]):
        print('ok')
        index = 2 * rd.randint(0, 2)
        res_str = ''
        for i in range(len(hex_str)):
            if i == index:
                char = str(rd.randint(0, 9))
            else:
                char = hex_str[i]
            res_str += char
        hex_str = res_str
    return '#' + hex_str


# To fetch files in a specified folder, returns the list of the paths to theses files
def fetch_files(dir_name='.', extension='.orpl', sub_dir=''):
    res = []
    path = dir_name + sub_dir
    for file in os.listdir(path):
        if extension in file:
            res += [path + '/' + file]
    return res


def fetch_from_dirs(list_dir, extension='.orpl', sub_dir=''):
    list_coord = []
    nb_folders = []
    for folder in list_dir:
        files = fetch_files(folder, extension, sub_dir)
        nb_folders += [len(files)]
        for f in files:
            list_coord += [[file_manager.get_coord(f), file_manager.get_param_from_file(f)]]
    return list_coord, nb_folders

# Get list of coordinates in an ORPL file (yaw,pitch_roll)
def get_coord(file_path):
    with open(file_path, "r") as f:
        data = f.readlines()

    yaw_l, pitch_l, roll_l = [], [], []

    data.pop(0)
    for i in range(len(data)):
        elems = data[i].split(" ")
        yaw_l.append(elems[0])
        pitch_l.append(elems[1])
        roll_l.append(elems[2])

    pitch_l = np.array(list(map(float, pitch_l)))
    yaw_l = np.array(list(map(float, yaw_l)))
    roll_l = np.array(list(map(float, roll_l)))

    return yaw_l, pitch_l, roll_l


# Convert n lists of m coordinates into a list of m n-dimensional vectors
def coord2points(data):
    n = len(data)
    m = len(data[0])
    points = []
    for i in range(m):
        point = []
        for j in range(n):
            point += [data[j][i]]
        points += [point]
    return points


def normalize(yaw_l, pitch_l, roll_l, type_norm='global'):
    """
    Normalize the data. This is done using the global maximum and minimum values of the
    three angles. For every value x, the normalized value is:
        (x-min)/(max-min)

    Parameters
    ----------
    pitch_l : list
            The pitch angles.
    roll_l : list
            The roll angles.
    yaw_l : list
            The yaw angles.
    type_norm : str
            For each of the possible values, the normalization of x is done as follows:
            'stat': (x-mean)/std
            'global': (x-global_min)/(global_max-global_min) (pitch & roll centered around 0.5)
            'local': (x-angle_min)/(angle_max-angle_min)

    Returns
    -------
    tuple
            Contains three lists, each corresponding to an angle, with the
            normalized value.
    """
    if type_norm == 'stat':
        normalized_pitch = (pitch_l - np.mean(pitch_l)) / np.std(pitch_l)
        normalized_yaw = (yaw_l - np.mean(yaw_l)) / np.std(yaw_l)
        normalized_roll = (roll_l - np.mean(roll_l)) / np.std(roll_l)
    elif type_norm == 'global':
        amin = np.amin([np.amin(pitch_l), np.amin(yaw_l), np.amin(roll_l)])
        amax = np.amax([np.amax(pitch_l), np.amax(yaw_l), np.amax(roll_l)])
        normalized_yaw = (yaw_l - amin) / (amax - amin)
        normalized_pitch = (pitch_l - amin) / (amax - amin)
        normalized_pitch = normalized_pitch - np.mean(normalized_pitch) + 0.5
        normalized_roll = (roll_l - amin) / (amax - amin)
        normalized_roll = normalized_roll - np.mean(normalized_roll) + 0.5
    elif type_norm == 'local':
        normalized_pitch = (pitch_l - np.amin(pitch_l)) / (np.amax(pitch_l) - np.amin(pitch_l))
        normalized_yaw = (yaw_l - np.amin(yaw_l)) / (np.amax(yaw_l) - np.amin(yaw_l))
        normalized_roll = (roll_l - np.amin(roll_l)) / (np.amax(roll_l) - np.amin(roll_l))
    else:
        raise ValueError('type_norm must take one of these values: "global", "local" or "stat"')
    return normalized_yaw, normalized_pitch, normalized_roll


def preprocess_data(array_data, type_norm='global'):
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
        norm_array.append(normalize(one_acq[0], one_acq[1], one_acq[2], type_norm))
    return norm_array
