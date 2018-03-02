"""
Script which allows to plot the superposition of a new data with the mean of the data base
"""

from Cervical_GUI.model.file_manager import get_param_from_file
from Cervical_GUI.model.plot_serie import *


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


def get_time_mean(list_patient, movement, angle, speed, nb_return, wait_time, norm=1):
    """
    Get the mean curves of the data base
    :param wait_time: wanted wait_time value
    :param nb_return: wanted nb_return value
    :param speed: wanted speed value
    :param angle: wanted angle value
    :param movement: wanted movement value
    :param list_patient: path which leads to the data base
    :param norm: optional, 1 if you want the data to be normed
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

        if norm:
            pitch_l, yaw_l, roll_l = normalize(pitch_l, yaw_l, roll_l)

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


def plot_final_time(current_file, list_patient, list_param, norm=1):
    """
    Plot the final figure : pitch vs pitch_mean, yaw vs yaw_mean, roll vs roll_mean, pitch vs yaw vs roll
    :param current_file: path which leads to the current file
    :param list_patient: list of every patient of the data_base
    :param list_param: list of parameters : movement, angle, speed,...
    :param norm: optional, 1 if you want the data to be normed
    :return: void
    """

    movement = list_param[0]
    angle = list_param[1]
    speed = list_param[2]
    nb_return = list_param[3]
    wait_time = list_param[4]
    pitch_mean, yaw_mean, roll_mean = get_time_mean(list_patient, movement, angle, speed, nb_return, wait_time, norm)

    pitch, yaw, roll = get_coord(current_file)

    fig_final, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(pitch)
    ax1.plot(pitch_mean)

    ax2.plot(yaw)
    ax2.plot(yaw_mean)

    ax3.plot(roll)
    ax3.plot(roll_mean)

    ax4.plot(pitch)
    ax4.plot(yaw)
    ax4.plot(roll)

    ax1.set_title("Pitch vs Pitch_mean")
    ax2.set_title("Yaw vs Yaw_mean")
    ax3.set_title("Roll vs Roll_mean")
    ax4.set_title("Pitch vs Yaw vs Roll")

    fig_final.show()
