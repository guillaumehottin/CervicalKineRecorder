# -*- coding: utf-8 -*-

""" Script d'affichage des données et sauvegarde des courbes :
- Affichage 3D
- Affichage des données temporelles
- Affichage des décompositions de fourrier respectives """

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pywt

from Code import myutils

directory = '../bonnes_mesures/'


def normalize(pitch_l, yaw_l, roll_l):
    """ Normalization of data
    :param pitch_l: tangage
    :param yaw_l: lacet
    :param roll_l: roulis
    :return: les données normalisées
    """
    amin = np.amin([np.amin(pitch_l), np.amin(yaw_l), np.amin(roll_l)])
    amax = np.amax([np.amax(pitch_l), np.amax(yaw_l), np.amax(roll_l)])
    normalized_pitch = (pitch_l - amin) / (amax - amin)
    normalized_yaw = (yaw_l - amin) / (amax - amin)
    normalized_roll = (roll_l - amin) / (amax - amin)
    return normalized_pitch, normalized_yaw, normalized_roll


def make_list_directory(dir_name):
    """ Construct the list of every patient folder's path
    :param dir_name: chemin vers le dossier des patients
    :return: list_path : liste de toutes les données
    """
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name + s for s in list_dir]  # contient la liste de tous les dossiers patients
    list_path = []
    for path in list_dir:
        list_path.extend(glob.glob(path + '/*.orpl'))
    return list_path


def get_wavelet(pitch_l, yaw_l, roll_l):
    pitch_a, pitch_d = pywt.dwt(pitch_l, 'db1')
    yaw_a, yaw_d = pywt.dwt(yaw_l, 'db1')
    roll_a, roll_d = pywt.dwt(roll_l, 'db1')
    return pitch_a, pitch_d, yaw_a, yaw_d, roll_a, roll_d


def get_fourrier(pitch_l, yaw_l, roll_l):
    fft_pitch = np.fft.fft(pitch_l)
    fft_yaw = np.fft.fft(yaw_l)
    fft_roll = np.fft.fft(roll_l)
    return fft_pitch, fft_yaw, fft_roll


def get_all_fourrier(dir_name, norm=1):
    list_path = make_list_directory(dir_name)
    all_fft_pitch = [[]]
    all_fft_yaw = [[]]
    all_fft_roll = [[]]
    for current_file in list_path:
        (pitch_l, yaw_l, roll_l) = myutils.get_coord(current_file)

        # Normalize data
        if norm:
            (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

        # Make fourrier decomposition
        fft_pitch, fft_yaw, fft_roll = get_fourrier(pitch_l, yaw_l, roll_l)

        all_fft_pitch.append(fft_pitch)
        all_fft_yaw.append(fft_yaw)
        all_fft_roll.append(fft_roll)

    return all_fft_pitch, all_fft_yaw, all_fft_roll


def plot_all_superposed_fourrier(dir_name, norm=1, save=0):
    """ Plot a figure with every fourrier decomposition superposed
    :param dir_name: chemin vers le dossiers des patients
    :param norm: optionel, 1 si on veut normer les données, 0 sinon
    :param save: pareil pour sauvegarder des figures
    """
    fig_superposed_fourrier, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig_superposed_fourrier.suptitle('Superposed Fourrier decomposition 1D')

    all_fft_pitch, all_fft_yaw, all_fft_roll = get_all_fourrier(dir_name, norm)

    for fft_pitch, fft_yaw, fft_roll in zip(all_fft_pitch, all_fft_yaw, all_fft_roll):
        ax1.plot(fft_yaw)
        ax2.plot(fft_pitch)
        ax3.plot(fft_roll)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')

    fig_superposed_fourrier.show()
    if save:
        if norm:
            fig_superposed_fourrier.savefig(dir_name + 'superposedNormedFft.png')
        else:
            fig_superposed_fourrier.savefig(dir_name + 'superposedFft.png')


def plot_one(current_file, type_plot, norm=1, save=0):
    assert type_plot == 'fourrier' or type_plot == '3d' or type_plot == 'time' or type_plot == 'wavelet'

    (pitch_l, yaw_l, roll_l) = myutils.get_coord(current_file)

    # Normalize data
    if norm:
        (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)

    if type_plot == 'fourrier':
        fft_pitch, fft_yaw, fft_roll = get_fourrier(pitch_l, yaw_l, roll_l)

        fig_fourrier, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        ax1.plot(fft_yaw)
        ax2.plot(fft_pitch)
        ax3.plot(fft_roll)
        ax1.set_title('yaw')
        ax2.set_title('pitch')
        ax3.set_title('roll')
        res_split = current_file.split('/')
        nom_patient = res_split[2]
        fig_fourrier.suptitle('Fourrier decomposition :' + nom_patient)

        if save:
            path = '/'.join(res_split[:-1])
            if norm:
                fig_fourrier.savefig(path + '/' + nom_patient + '_norm_fourrier.png')
            else:
                fig_fourrier.savefig(path + '/' + nom_patient + '_fourrier.png')

        fig_fourrier.show()

    elif type_plot == '3d':
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

    elif type_plot == 'time':
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

    elif type_plot == 'wavelet':
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


def plot_all(dir_name, type_plot, norm=1, save=0):
    list_path = make_list_directory(dir_name)

    for current_file in list_path:
        plot_one(current_file, type_plot, norm, save)


liste = make_list_directory(directory)
# plot_all(directory, 'time')
plot_all_superposed_fourrier(directory, save=0, norm=1)
# plot_one(liste[0], 'wavelet', save=1, norm=0)
