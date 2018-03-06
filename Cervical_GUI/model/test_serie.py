"""
Script de test des fonctions du fichier model.plot_serie.py
"""
from model.plot_serie import *

directory = '../../bonnes_mesures/'

liste = get_list_directory(directory)
# plot_all_superposed_correlate(directory)
# plot_all_superposed_fourier(directory)
# plot_one(liste[0], type_plot='correlate')
# plot_one(liste[0])
plot_one(liste[0], type_plot='time')

# plot_one(liste[0], type_plot='3d', type_wavelet='db1')
# for family in pywt.families():
#     for wave in pywt.wavelist(family):
#         plot_one(liste[0], type_wavelet=wave, type_plot='wavelet')
# plot_one(liste[0], type_wavelet='morl', type_plot='wavelet')
# plot_one(liste[0], type_plot='time')
# plot_one(liste[0], type_plot='fourier')
# plot_one(liste[0], type_plot='3d')
# plot_one(liste[0], type_plot='correlate')

# plot_all_superposed_wavelet(directory, type_wavelet='morl', norm=0, save=0)
# plot_one(elem, type_wavelet='morl', type_plot='wavelet')
# for elem in liste:
#     plot_one(elem, type_plot='time')
#     plot_one(elem, type_plot='fourier')
#     plot_one(elem, type_plot='wavelet')
#     plot_one(elem, type_plot='correlate')
#     plot_one(elem, type_plot='3d')
#     time.sleep(5)

# plot_all_superposed_wavelet(directory, type_wavelet='morl')

# plot_all(directory, type_plot='time')
# (pitch_l, yaw_l, roll_l) = get_coord(liste[0])
# (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)
# fig = plt.figure()
# plt.xlim((0, 1))
# plt.ylim((0, 1))
# plt.plot(yaw_l, pitch_l)
# plt.show()
