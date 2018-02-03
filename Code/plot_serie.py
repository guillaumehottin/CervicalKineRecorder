import matplotlib.pyplot as plt
import numpy as np
import os
import myutils
import re
from mpl_toolkits.mplot3d import Axes3D
import glob

motion = ['Lacet','Roulis']
dir_name = '../bonnes_mesures/'
list_dir = next(os.walk(dir_name))[1]
list_dir = [dir_name+s for s in list_dir]
list_path=[]

for path in list_dir:
	list_path.extend(glob.glob(path+'/*.orpl'))


(pitch_l, yaw_l, roll_l) = myutils.get_coord(list_path[3])
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
plt.xlabel('yaw')
plt.ylabel('pitch')

ax.plot(yaw_l,pitch_l,roll_l)
fig1.show()

fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
l = np.linspace(0,len(yaw_l), len(yaw_l))
ax1.scatter(l, yaw_l)
ax2.scatter(l, pitch_l)
ax3.scatter(l, roll_l)
fig2.show()
input()
