# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os
import myutils
import glob
#from mpl_toolkits.mplot3d import Axes3D


def normalize(pitch_l,yaw_l,roll_l):
#	normalized_pitch = (pitch_l-np.amin(pitch_l))/(np.amax(pitch_l)-np.amin(pitch_l))
#	normalized_yaw = (yaw_l-np.amin(yaw_l))/(np.amax(yaw_l)-np.amin(yaw_l))
#	normalized_roll = (roll_l-np.amin(roll_l))/(np.amax(roll_l)-np.amin(roll_l))
    normalized_pitch = pitch_l/np.linalg.norm(pitch_l)
    normalized_yaw = yaw_l/np.linalg.norm(yaw_l)
    normalized_roll = roll_l/np.linalg.norm(roll_l)
    return normalized_pitch,normalized_yaw,normalized_roll

motion = ['Lacet','Roulis']
dir_name = '../bonnes_mesures/'
list_dir = next(os.walk(dir_name))[1]
list_dir = [dir_name+s for s in list_dir]

list_path=[]
for path in list_dir:
	list_path.extend(glob.glob(path+'/*.orpl'))

save = 0
norm = 1
fig3, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
for current_file in list_path:
    # current_file = list_path[0]
    (pitch_l, yaw_l, roll_l) = myutils.get_coord(current_file)
    # =============================================================================
    # PLOT 3D
    #     fig1 = plt.figure()
    #     ax = fig1.add_subplot(111, projection='3d')
    #     plt.xlabel('yaw')
    #     plt.ylabel('pitch')
    #     ax.plot(yaw_l,pitch_l,roll_l)
    #     fig1.show()
    #     name = elem + '_3D' + '.png'
    #     plt.savefig(name)
    # =============================================================================
    
    # =============================================================================
    # SAVE Courbes
    #     if save:
    #         fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    #         l = np.linspace(0,len(yaw_l), len(yaw_l))
    #         ax1.scatter(l, yaw_l)
    #         ax2.scatter(l, pitch_l)
    #         ax3.scatter(l, roll_l)
    #         fig2.show()
    #         name = current_file + '.png'
    #         plt.savefig(name)
    # =============================================================================
    ## Normalize data
    if norm:
        (pitch_l, yaw_l, roll_l) = normalize(pitch_l, yaw_l, roll_l)
        
    ## Transformée de fourrier
    fft_pitch = np.fft.fft(pitch_l)
    fft_yaw = np.fft.fft(yaw_l)
    fft_roll = np.fft.fft(roll_l)
    ax1.plot(fft_yaw)
    ax2.plot(fft_pitch)
    ax3.plot(fft_roll)
    
plt.legend()
ax1.set_title('yaw')
ax2.set_title('pitch')
ax3.set_title('roll')
fig3.suptitle('Fourrier decomposition')
if norm:
    name = '../Figures/superposed_norm_Fourrier.png'
else:
    name = name = '../Figures/superposed_Fourrier.png'
plt.savefig(name)
plt.show()
