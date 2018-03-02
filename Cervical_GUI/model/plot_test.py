#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Created on Thu Feb  8 11:59:33 2018

@author: lsapin
"""
import numpy as np
import matplotlib.pyplot as plt
from model import myutils

(pitch_l, yaw_l, roll_l) = myutils.get_coord('test.txt')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.plot(yaw_l, pitch_l)
ax2.plot(pitch_l, roll_l)
ax3.plot(roll_l, yaw_l, color='r')
ax1.set_title('pitch = f(yaw)')	
ax2.set_title('roll = f(pitch)')
ax3.set_title('yaw = f(roll)')
plt.show()

fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
plt.xlabel('pitch')
plt.ylabel('roll')
ax.plot(pitch_l,roll_l,yaw_l)
fig1.show()
input()

## Transformée de fourrier
fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplot(2, 2)
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
