"""
Script which allows to plot the superposition of a new data with the mean of the data base
"""
import datetime

<<<<<<< HEAD
from model.file_manager import get_param_from_file
from model.plot_serie import *
from model.myutils import *
=======
from Cervical_GUI.model.plot_serie import *
from Cervical_GUI.model.myutils import *
>>>>>>> b7c14719b69faea09d9dbbd3d48720b7c513c072


def get_list_patient(dir_name):
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name + s for s in list_dir]  # contient la liste de tous les dossiers patients
    return list_dir


def get_list_data(array_data):
    """
    Get a list of data = liste of .orpl files
    :param array_data: list of directory, corresponding to different patient
    :return: list of .orpl files
    """
    list_path = []
    for path in array_data:
        list_path.extend(glob.glob(path + '/*.orpl'))
    return list_path


def get_all_param(array_data):
    """
    Get all the parameters from a list of data
    :param array_data: list of files containing data
    :return: lists of every parameters : movements, angles, speeds...
    """
    movements = []
    angles = []
    speeds = []
    nb_returns = []
    wait_times = []
    comments = []
    for acq in array_data:
        print(acq)
        movement, angle, speed, nb_return, wait_time, comment = acq[1]
        movements.append(movement)
        angles.append(angle)
        speeds.append(speed)
        nb_returns.append(nb_return)
        wait_times.append(wait_time)
        comments.append(comment)
    return movements, angles, speeds, nb_returns, wait_times, comments


def get_same_param_data(array_data, movement, angle, speed, nb_return, wait_time):
    """
    Get the list of data which has the same parameters
    :param array_data: a list of directories containing data files
    :param movement: wanted movement
    :param angle: wanted angle
    :param speed: wanted speed
    :param nb_return: wanted nb_return
    :param wait_time: wanted wait_time
    :return: the list of data with the same parameters
    """
    # list_data = get_list_data(array_data)

    movements, angles, speeds, nb_returns, wait_times, comments = get_all_param(array_data)
    indices_to_remove = []
    for i in range(len(movements) - 1):
        same_param = movement == movements[i + 1] and angle == angles[i + 1] and speed == speeds[i + 1] \
                     and nb_return == nb_returns[i + 1] and wait_time == wait_times[i + 1]
        if not same_param:
            indices_to_remove += [i]
        movement = movements[i+1]
        angle = angles[i+1]
        speed = speeds[i+1]
        nb_return = nb_returns[i+1]
        wait_time = wait_times[i+1]
    for i in reversed(indices_to_remove):
        array_data.pop(i)
    return array_data


def get_time_mean(array_data, list_param):
    """
    Get the mean curves of the data base
    :param list_param: list of parameters : movement, angle, speed,...
    :param array_data: path which leads to the data base
    :return: (mean_pitch, mean_yaw, mean_roll) three lists representing the mean curves of the data base
    """

    # On récupère la liste des données qui ont les mêmes paramètres
    movement = list_param[0]
    angle = list_param[1]
    speed = list_param[2]
    nb_return = list_param[3]
    wait_time = list_param[4]
    list_file = get_same_param_data(array_data, movement, angle, speed, nb_return, wait_time)
    all_pitch = []
    all_yaw = []
    all_roll = []
    for current_file in list_file:
        # on récupère les coordonnées spatiales des données
        pitch_l, yaw_l, roll_l = current_file[0]

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


def save_model(list_patient, directory, norm=True):
    list_data = fetch_from_dirs(list_patient)[0]
    movement, angle, speed, nb_return, wait_time, comments = list_data[0][1]
    list_param = [movement, angle, speed, nb_return, wait_time] 
    if norm:
        list_data = [[y, z[1]] for y, z in zip (preprocess_data([x[0] for x in list_data]), list_data)]

    pitch_mean, yaw_mean, roll_mean = get_time_mean(list_data, list_param)

    now = datetime.datetime.now()
    file_name = directory + '/time_serie_' + now.strftime("%m-%d-%Y_%H%M") + '.mdlwvl'
    with open(file_name, 'w+') as file:
        file.write(str(movement) + '\n' + str(angle) + '\n' + str(speed) + '\n' + str(nb_return) + '\n' +
                   str(wait_time) + '\n')

        file.write('yaw \t pitch \t roll \n')
        for pitch, yaw, roll in zip(pitch_mean, yaw_mean, roll_mean):
            file.write(str(yaw) + '\t' + str(pitch) + '\t' + str(roll) + '\n')


def plot_final_time(current_file, array_data, list_param, norm=1):
    """
    Plot the final figure : pitch vs pitch_mean, yaw vs yaw_mean, roll vs roll_mean, pitch vs yaw vs roll
    :param current_file: path which leads to the current file
    :param array_data: list of every patient of the data_base
    :param list_param: list of parameters : movement, angle, speed,...
    :param norm: optional, 1 if you want the data to be normed
    :return: void
    """

    pitch_mean, yaw_mean, roll_mean = get_time_mean(array_data, list_param, norm)

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


def load_model(model_path):
    with open(model_path, 'r+') as file:
        data = file.readlines()
        list_param = [data[0], data[1], data[2], data[3], data[4]]
        yaw = []
        pitch = []
        roll = []
        for i in range(6, len(data)):
            tmp = data[i].split('\t')
            yaw.append(tmp[0])
            pitch.append(tmp[1])
            roll.append(tmp[2])
    return yaw, pitch, roll, list_param


# Script pour créer un modèle test à partir d'une liste de patients test
# Chemin vers le(s) dossier(s) contenant les données :
list_patient = ['~/Documents/']