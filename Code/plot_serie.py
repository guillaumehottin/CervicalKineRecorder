# -*- coding: utf-8 -*-

""" Script d'affichage des données et sauvegarde des courbes :
- Affichage 3D
- Affichage des données temporelles
- Affichage des décompositions de fourier respectives """

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pywt

from Code.myutils import get_coord
from mpl_toolkits.mplot3d import Axes3D


def normalize(pitch_l, yaw_l, roll_l):
    """ Normalization of data
    :param pitch_l: list of pitch movement
    :param yaw_l: list of yaw movement
    :param roll_l: list of roll movement
    :return: 3 lists, 1 for each movement, filled with normalized data
    """
    amin = np.amin([np.amin(pitch_l), np.amin(yaw_l), np.amin(roll_l)])
    amax = np.amax([np.amax(pitch_l), np.amax(yaw_l), np.amax(roll_l)])
    normalized_pitch = (pitch_l - amin) / (amax - amin)
    normalized_yaw = (yaw_l - amin) / (amax - amin)
    normalized_roll = (roll_l - amin) / (amax - amin)
    return normalized_pitch, normalized_yaw, normalized_roll


def save_fig(fig, res_split, norm, type_plot):
    path = '/'.join(res_split[:-1])
    nom_patient = res_split[2]
    if norm:
        fig.savefig(path + '/' + nom_patient + '_norm_' + type_plot + '.png')
    else:
        fig.savefig(path + '/' + nom_patient + '_' + type_plot + '.png')


def get_list_directory(dir_name):
    """ Construct the list of every patient folder's path
    :param dir_name: path which leads to the data base
    :return: list_path : list of each path of each data
    """
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name + s for s in list_dir]  # contient la liste de tous les dossiers patients
    list_path = []
    for path in list_dir:
        list_path.extend(glob.glob(path + '/*.txt'))
    return list_path


def get_wavelet(pitch_l, yaw_l, roll_l, type_wavelet):
    """
    Calculates wavelet transformation for each movement list
    :param type_wavelet: type of the wavelet family used
    :param pitch_l: list of pitch movement
    :param yaw_l: list of yaw movement
    :param roll_l: list of roll movement
    :return: for each list, returns 2 list corresponding to the wavelet transformation
    ex : (pitch_coef, pitch_freq) for pitch_l, etc...
    """
    scale = 2*np.sqrt(len(yaw_l))
    pitch_coef, pitch_freq = pywt.cwt(pitch_l, scale, type_wavelet)
    yaw_coef, yaw_freq = pywt.cwt(yaw_l, scale, type_wavelet)
    roll_coef, roll_freq = pywt.cwt(roll_l, scale, type_wavelet)
    return pitch_coef, pitch_freq, yaw_coef, yaw_freq, roll_coef, roll_freq


def get_fourier(pitch_l, yaw_l, roll_l):
    """
    Calculate the fourier transformation of a data set
    :param pitch_l: pitch data list
    :param yaw_l: yaw data list
    :param roll_l: roll data list
    :return: 3 lists corresponding to the fourier transformation of each data.
    """
    fft_pitch = np.fft.fft(pitch_l)
    fft_yaw = np.fft.fft(yaw_l)
    fft_roll = np.fft.fft(roll_l)
    return fft_pitch, fft_yaw, fft_roll


def get_correlate(pitch_l, yaw_l, roll_l, mode='same'):
    """
    Calculates the correlation between 2 normalized signals
    :param pitch_l: pitch data movement
    :param yaw_l: yaw data movement
    :param roll_l: roll data movement
    :param mode: optional. refer to the convolve docstring
    :return: correlation between each pair of movement
    """

    pitch_yaw = np.correlate(pitch_l, yaw_l, mode=mode)
    pitch_roll = np.correlate(pitch_l, roll_l, mode=mode)
    roll_yaw = np.correlate(roll_l, yaw_l, mode=mode)

    return pitch_yaw, pitch_roll, roll_yaw


def get_all_fourier(dir_name, norm=1):
    """
    Calculates and returns every fourier decomposition of a data base
    :param dir_name: path which leads to the data base
    :param norm: optional, 1 if you want to norm your data base, 0 if not.
    :return: returns every fourier decomposition of a data base, for each movement.
    """
    list_path = get_list_directory(dir_name)
    all_fft_pitch = []
    all_fft_yaw = []
    all_fft_roll = []
    for current_file in list_path:
        (pitch_l, yaw_l, roll_l) = get_coord(current_file)

        # Normalize data
        if norm:
            (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

        # Make fourier decomposition
        fft_pitch, fft_yaw, fft_roll = get_fourier(pitch_l, yaw_l, roll_l)

        all_fft_pitch.append(fft_pitch)
        all_fft_yaw.append(fft_yaw)
        all_fft_roll.append(fft_roll)

    return all_fft_pitch, all_fft_yaw, all_fft_roll


def get_all_correlate(dir_name, norm=1, mode='same'):
    """
    Get all the correlation data of the data base
    :param dir_name: path which leads to the data base
    :param norm: optional, 1 if you want the data to be normed
    :param mode: optional, 1 if you want the figures to be saved
    :return: 3 lists of list, one for each movement, for all the data base. One element of a list is for one patient.
    """
    list_path = get_list_directory(dir_name)
    all_corr_pitch_yaw = []
    all_corr_pitch_roll = []
    all_corr_roll_yaw = []
    for current_file in list_path:
        (pitch_l, yaw_l, roll_l) = get_coord(current_file)

        # Normalize data
        if norm:
            (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

        # Make fourier decomposition
        pitch_yaw, pitch_roll, roll_yaw = get_correlate(pitch_l, yaw_l, roll_l, mode)

        all_corr_pitch_yaw.append(pitch_yaw)
        all_corr_pitch_roll.append(pitch_roll)
        all_corr_roll_yaw.append(roll_yaw)

    return all_corr_pitch_yaw, all_corr_pitch_roll, all_corr_roll_yaw


def get_all_wavelet(dir_name, type_wavelet='morl', norm=1):
    list_path = get_list_directory(dir_name)
    all_wavelet_pitch = []
    all_wavelet_yaw = []
    all_wavelet_roll = []
    for current_file in list_path:
        (pitch_l, yaw_l, roll_l) = get_coord(current_file)

        # Normalize data
        if norm:
            (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

        # Make fourier decomposition
        pitch_coef, pitch_freq, yaw_coef, yaw_freq, roll_coef, roll_freq = get_wavelet(pitch_l, yaw_l, roll_l, type_wavelet)

        all_wavelet_pitch.append(pitch_coef)
        all_wavelet_yaw.append(yaw_coef)
        all_wavelet_roll.append(roll_coef)

    return all_wavelet_pitch, all_wavelet_yaw, all_wavelet_roll


def plot_all_superposed_fourier(dir_name, norm=1, save=0):
    """ Plot a figure with every fourier decomposition superposed
    :param dir_name: path which leads to the data base
    :param norm: optional, 1 if you want to norm data, 0 if not
    :param save: optional, 1 if you want to save figures, 0 if not
    """
    fig_superposed_fourier, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig_superposed_fourier.suptitle('Superposed fourier decomposition 1D')

    all_fft_pitch, all_fft_yaw, all_fft_roll = get_all_fourier(dir_name, norm)

    for fft_pitch, fft_yaw, fft_roll in zip(all_fft_pitch, all_fft_yaw, all_fft_roll):
        ax1.plot(fft_yaw)
        ax2.plot(fft_pitch)
        ax3.plot(fft_roll)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')

    fig_superposed_fourier.show()
    if save:
        if norm:
            fig_superposed_fourier.savefig(dir_name + 'superposedNormedFft.png')
        else:
            fig_superposed_fourier.savefig(dir_name + 'superposedFft.png')


def plot_all_superposed_correlate(dir_name, norm=1, save=0, mode='same'):
    """
    Plot a figure with every correlation of the data base
    :param dir_name: path which leads to the data base
    :param norm: optional, 1 if you want the data to be normed
    :param save: optional, 1 if you want the figures to be saved
    :param mode: optional, 'same' as default, 'valid', 'full'
    :return:
    """
    fig_superposed_correlate, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig_superposed_correlate.suptitle('Superposed Correlations')

    all_corr_pitch_yaw, all_corr_pitch_roll, all_corr_roll_yaw = get_all_correlate(dir_name, norm, mode)

    for pitch_yaw, pitch_roll, roll_yaw in zip(all_corr_pitch_yaw, all_corr_pitch_roll, all_corr_roll_yaw):
        ax1.plot(pitch_yaw)
        ax2.plot(pitch_roll)
        ax3.plot(roll_yaw)

        ax1.set_title('yaw x pitch')
        ax2.set_title('roll x pitch')
        ax3.set_title('roll x yaw')

    fig_superposed_correlate.show()
    if save:
        if norm:
            fig_superposed_correlate.savefig(dir_name + 'superposedNormedCorrelate.png')
        else:
            fig_superposed_correlate.savefig(dir_name + 'superposedCorrelate.png')


def plot_all_superposed_wavelet(dir_name, type_wavelet, norm=1, save=0):
    fig_superposed_wavelet, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig_superposed_wavelet.suptitle('Superposed wavelet decomposition 1D')

    all_wavelet_pitch, all_wavelet_yaw, all_wavelet_roll = get_all_wavelet(dir_name, type_wavelet, norm)

    for pitch_coef, yaw_coef, roll_coef in zip(all_wavelet_pitch, all_wavelet_yaw, all_wavelet_roll):
        ax1.plot(pitch_coef[0])
        ax2.plot(yaw_coef[0])
        ax3.plot(roll_coef[0])
        # print(pitch_coef)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')

        fig_superposed_wavelet.show()

    if save:
        if norm:
            fig_superposed_wavelet.savefig(dir_name + 'superposedNormedWavelet.png')
        else:
            fig_superposed_wavelet.savefig(dir_name + 'superposedWavelet.png')


def plot_one(current_file, type_plot, type_wavelet='morl', norm=1, save=0):
    """
    Plot curves corresponding to a single data set
    :param type_wavelet: type of the wavelet family used
    :param current_file: path which leads to the data set
    :param type_plot: which type of ploting : fourier decomposition, time movement, 3d movement, wavelet transformation,correlation
    :param norm: optional, 1 if you want to norm your data set, 0 if not
    :param save: optional, 1 if you want to save the figures, 0 if not
    :return: Void
    """
    assert type_plot == 'fourier' or type_plot == '3d' or type_plot == 'time' or type_plot == 'wavelet' \
           or type_plot == 'correlate'

    res_split = current_file.split('/')
    nom_patient = res_split[3]
    fig = plt.figure()

    (pitch_l, yaw_l, roll_l) = get_coord(current_file)

    # Normalize data
    if norm:
        (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

    if type_plot == 'fourier':
        fft_pitch, fft_yaw, fft_roll = get_fourier(pitch_l, yaw_l, roll_l)

        plt.plot(fft_yaw, 'r')
        plt.plot(fft_pitch, 'b')
        plt.plot(fft_roll, 'g')
        plt.legend(['Yaw', 'Pitch', 'Roll'])

        title = 'Fourier decomposition'

    elif type_plot == '3d':
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(yaw_l, pitch_l, roll_l)

        plt.xlabel('yaw')
        plt.ylabel('pitch')
        plt.legend(['3d movement'])
        type_plot = '3d representation'

        title = '3d'

    elif type_plot == 'time':
        abscisses = np.linspace(0, len(yaw_l), len(yaw_l))
        plt.plot(abscisses, yaw_l, 'r')
        plt.plot(abscisses, pitch_l, 'b')
        plt.plot(abscisses, roll_l, 'g')
        plt.legend(['Yaw', 'Pitch', 'Roll'])

        title = 'Time data'

    elif type_plot == 'wavelet':
        pitch_coef, pitch_freq, yaw_coef, yaw_freq, roll_coef, roll_freq = get_wavelet(pitch_l, yaw_l, roll_l,
                                                                                       type_wavelet)
        plt.plot(yaw_coef[0], 'r')
        plt.plot(pitch_coef[0], 'b')
        plt.plot(roll_coef[0], 'g')
        plt.legend(['Yaw', 'Pitch', 'Roll'])

        title = 'Wavelet decomposition, ' + type_wavelet

    elif type_plot == 'correlate':
        pitch_yaw, pitch_roll, roll_yaw = get_correlate(pitch_l, yaw_l, roll_l, mode='same')

        plt.plot(pitch_yaw, 'r')
        plt.plot(pitch_roll, 'b')
        plt.plot(roll_yaw, 'g')
        plt.legend(['Pitch x Yaw', 'Pitch x Roll', 'Roll x Yaw'])

        title = 'Correlation'

    fig.suptitle(title + ': ' + nom_patient)
    plt.show()

    if save:
        save_fig(fig, res_split, norm, type_plot)


def plot_all(dir_name, type_plot, type_wavelet='morl', norm=1, save=0):
    """
    Plot all the data base in a row
    :param type_wavelet: type of the wavelet used
    :param dir_name: path which leads to the data base
    :param type_plot: type of plotting : 3d, Time, fourier, Wavelet
    :param norm: optional, 1 if you want to norm each data, 0 if not
    :param save: optional, 1 if you want to save the figures, 0 if not
    :return: void
    """
    list_path = get_list_directory(dir_name)

    for current_file in list_path:
        plot_one(current_file, type_plot=type_plot, type_wavelet=type_wavelet, norm=norm, save=save)
