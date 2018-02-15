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
from scipy import signal

directory = '../bonnes_mesures/'


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


def get_list_directory(dir_name):
    """ Construct the list of every patient folder's path
    :param dir_name: path which leads to the data base
    :return: list_path : list of each path of each data
    """
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name + s for s in list_dir]  # contient la liste de tous les dossiers patients
    list_path = []
    for path in list_dir:
        list_path.extend(glob.glob(path + '/*.orpl'))
    return list_path


def get_wavelet(pitch_l, yaw_l, roll_l):
    """
    Calculates wavelet transformation for each movement list
    :param pitch_l: list of pitch movement
    :param yaw_l: list of yaw movement
    :param roll_l: list of roll movement
    :return: for each list, returns 2 list corresponding to the wavelet transformation
    ex : (pitch_a, pitch_d) for pitch_l, etc...
    """
    pitch_a, pitch_d = pywt.dwt(pitch_l, 'db1')
    yaw_a, yaw_d = pywt.dwt(yaw_l, 'db1')
    roll_a, roll_d = pywt.dwt(roll_l, 'db1')
    return pitch_a, pitch_d, yaw_a, yaw_d, roll_a, roll_d


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


def get_all_fourier(dir_name, norm=1):
    """
    Calculates and returns every fourier decomposition of a data base
    :param dir_name: path which leads to the data base
    :param norm: optional, 1 if you want to norm your data base, 0 if not.
    :return: returns every fourier decomposition of a data base, for each movement.
    """
    list_path = get_list_directory(dir_name)
    all_fft_pitch = [[]]
    all_fft_yaw = [[]]
    all_fft_roll = [[]]
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


def plot_one(current_file, type_plot='fourier', norm=1, save=0):
    """
    Plot curves corresponding to a single data set
    :param current_file: path which leads to the data set
    :param type_plot: which type of ploting : fourier decomposition, time movement, 3d movement, wavelet transformation
    :param norm: optional, 1 if you want to norm your data set, 0 if not
    :param save: optional, 1 if you want to save the figures, 0 if not
    :return: Void
    """
    assert type_plot == 'fourier' or type_plot == '3d' or type_plot == 'time' or type_plot == 'wavelet' \
        or type_plot == 'correlate'

    (pitch_l, yaw_l, roll_l) = get_coord(current_file)

    # Normalize data
    if norm:
        (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

    if type_plot == 'fourier':
        fft_pitch, fft_yaw, fft_roll = get_fourier(pitch_l, yaw_l, roll_l)

        fig_fourier, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        ax1.plot(fft_yaw)
        ax2.plot(fft_pitch)
        ax3.plot(fft_roll)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')
        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig_fourier.suptitle('fourier decomposition :' + nom_patient)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig_fourier.savefig(path + '/' + nom_patient + '_norm_fourier.png')
            else:
                fig_fourier.savefig(path + '/' + nom_patient + '_fourier.png')

        fig_fourier.show()

    if type_plot == '3d':
        fig3d = plt.figure()
        ax = fig3d.add_subplot(111, projection='3d')
        plt.xlabel('yaw')
        plt.ylabel('pitch')
        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig3d.suptitle('Représentation 3d: ' + nom_patient)
        ax.plot(yaw_l, pitch_l, roll_l)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig3d.savefig(path + '/' + nom_patient + '_norm_3D.png')
            else:
                fig3d.savefig(path + '/' + nom_patient + '_3D.png')

        fig3d.show()

    if type_plot == 'time':
        fig_time, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        abscisses = np.linspace(0, len(yaw_l), len(yaw_l))
        ax1.plot(abscisses, yaw_l)
        ax2.plot(abscisses, pitch_l)
        ax3.plot(abscisses, roll_l)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')
        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig_time.suptitle('Time data: ' + nom_patient)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig_time.savefig(path + '/' + nom_patient + '_norm_timedata.png')
            else:
                fig_time.savefig(path + '/' + nom_patient + '_timedata.png')

        fig_time.show()

    if type_plot == 'wavelet':
        pitch_a, pitch_d, yaw_a, yaw_d, roll_a, roll_d = get_wavelet(pitch_l, yaw_l, roll_l)

        fig_wavelet, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        ax1.plot(yaw_a, yaw_d)
        ax2.plot(pitch_a, pitch_d)
        ax3.plot(roll_a, roll_d)

        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')

        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig_wavelet.suptitle('Wavelet decomposition :' + nom_patient)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig_wavelet.savefig(path + '/' + nom_patient + '_norm_wavelet.png')
            else:
                fig_wavelet.savefig(path + '/' + nom_patient + '_wavelet.png')

        fig_wavelet.show()

    if type_plot == 'correlate':
        pitch_yaw, pitch_roll, roll_yaw = correlate(pitch_l, yaw_l, roll_l, mode='valid')

        fig_correlate, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        ax1.plot(pitch_yaw)
        ax2.plot(pitch_roll)
        ax3.plot(roll_yaw)

        ax1.set_title('yaw x pitch')
        ax2.set_title('roll x pitch')
        ax3.set_title('roll x yaw')

        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig_correlate.suptitle('Correlation :' + nom_patient)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig_correlate.savefig(path + '/' + nom_patient + '_norm_correlation.png')
            else:
                fig_correlate.savefig(path + '/' + nom_patient + '_correlation.png')

        plt.show()


def plot_all(dir_name, type_plot, norm=1, save=0):
    """
    Plot all the data base in a row
    :param dir_name: path which leads to the data base
    :param type_plot: type of plotting : 3d, Time, fourier, Wavelet
    :param norm: optional, 1 if you want to norm each data, 0 if not
    :param save: optional, 1 if you want to save the figures, 0 if not
    :return: void
    """
    list_path = get_list_directory(dir_name)

    for current_file in list_path:
        plot_one(current_file, type_plot, norm, save)


def correlate(pitch_l, yaw_l, roll_l, mode='valid'):
    """
    Calculates the correlation between 2 normalized signals
    :param pitch_l: pitch data movement
    :param yaw_l: yaw data movement
    :param roll_l: roll data movement
    :param mode: optional. refer to the convolve docstring
    :return: correlation between each pair of movement
    """

    pitch_yaw = signal.fftconvolve(pitch_l, yaw_l, mode=mode)
    pitch_roll = signal.fftconvolve(pitch_l, roll_l, mode=mode)
    roll_yaw = signal.fftconvolve(roll_l, yaw_l, mode=mode)

    return pitch_yaw, pitch_roll, roll_yaw


liste = get_list_directory(directory)
# plot_all(directory, 'time')
# plot_all_superposed_fourier(directory, save=0, norm=1)
plot_one(liste[0], type_plot='correlate')
