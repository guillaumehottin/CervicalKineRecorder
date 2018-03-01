"""
Script which allows to plot the superposition of a new data with the mean of the data base
"""
import glob
import os

from Code.myutils import get_coord
from Cervical_GUI.model.file_manager import get_param_from_file


def get_list_patient(dir_name):
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name + s for s in list_dir]  # contient la liste de tous les dossiers patients
    return list_dir


def get_list_data(liste_patient):
    """
    Get a list of data = liste of .orpl files
    :param liste_patient: list of directory, corresponding to different patient
    :return: list of .orpl files
    """
    list_path = []
    for path in liste_patient:
        list_path.extend(glob.glob(path + '/*.orpl'))
    return list_path


def get_all_param(list_data):
    """
    Get all the parameters from a list of data
    :param list_data: list of files containing data
    :return: lists of every parameters : movements, angles, speeds...
    """
    movements = []
    angles = []
    speeds = []
    nb_returns = []
    wait_times = []
    comments = []
    for file in list_data:
        [movement, angle, speed, nb_return, wait_time, comment] = get_param_from_file(file)
        movements.append(movement)
        angles.append(angle)
        speeds.append(speed)
        nb_returns.append(nb_return)
        wait_times.append(wait_time)
        comments.append(comment)
    return movements, angles, speeds, nb_returns, wait_times, comments


def get_same_param_data(list_patient, movement, angle, speed, nb_return, wait_time):
    """
    Get the list of data which has the same parameters
    :param list_patient: a list of directories containing data files
    :param movement: wanted movement
    :param angle: wanted angle
    :param speed: wanted speed
    :param nb_return: wanted nb_return
    :param wait_time: wanted wait_time
    :return: the list of data with the same parameters
    """
    list_data = get_list_data(list_patient)
    movements, angles, speeds, nb_returns, wait_times, comments = get_all_param(list_data)

    for i in range(len(movements) - 1):
        same_param = movement == movements[i + 1] and angle == angles[i + 1] and speed == speeds[i + 1] \
                     and nb_return == nb_returns[i + 1] and wait_time == wait_times[i + 1]
        if not same_param:
            list_data.pop(i)
    return list_data


def get_time_mean(list_patient, movement, angle, speed, nb_return, wait_time, norm=1, save=0):
    """
    Get the mean curves of the data base
    :param wait_time: wanted wait_time value
    :param nb_return: wanted nb_return value
    :param speed: wanted speed value
    :param angle: wanted angle value
    :param movement: wanted movement value
    :param list_patient: path which leads to the data base
    :param norm: optional, 1 if you want the data to be normed
    :param save: optional, 1 if you want to save the figures
    :return: (mean_pitch, mean_yaw, mean_roll) three lists representing the mean curves of the data base
    """

    # On récupère la liste des données qui ont les mêmes paramètres
    list_file = get_same_param_data(list_patient, movement, angle, speed, nb_return, wait_time)
    all_pitch = []
    all_yaw = []
    all_roll = []
    for current_file in list_file:
        # on récupère les coordonnées spatiales des données
        pitch_l, yaw_l, roll_l = get_coord(current_file)

        all_pitch.append(pitch_l)
        all_yaw.append(yaw_l)
        all_roll.append(roll_l)

    # all_pitch, all_yaw and all_roll contains all time data with the same parameters

    # calcul des courbes moyennes
    mean_pitch = [0]*len(all_pitch[0])
    mean_yaw = [0]*len(all_yaw[0])
    mean_roll = [0]*len(all_roll[0])

    for i in range(len(mean_pitch)):
        for j in range(len(all_pitch)):
            mean_pitch[i] += all_pitch[j][i]/len(all_pitch)
            mean_yaw[i] += all_yaw[j][i]/len(all_yaw)
            mean_roll[i] += all_roll[j][i]/len(all_roll)

    return mean_pitch, mean_yaw, mean_roll