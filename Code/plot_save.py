import matplotlib.pyplot as plt
import numpy as np
import os

def get_coord(file_path):
	f = open(file_path,"r")
	data = f.readlines()
	yaw_l, pitch_l, roll_l = [],[],[]

	data.pop(0)
	for i in range(0,len(data)):
		elems = data[i].split(" ")
		yaw_l.append(elems[0])
		pitch_l.append(elems[1])
		roll_l.append(elems[2])

	pitch_l = list(map(float, pitch_l))
	yaw_l = list(map(float, yaw_l))
	roll_l = list(map(float, roll_l))
	return (pitch_l,yaw_l,roll_l)

def plot_from_file(name_file,name_dir,save_fig=0,show=1,scatter=0):
    (pitch_l,yaw_l,roll_l) = get_coord(name_dir+'\\'+name_file)
    fig = plot_figs(pitch_l,yaw_l,roll_l,show,scatter)
    if save_fig:
        new_name = (name_dir+'\\'+name_file).split(".")[0] + ".png"
        plt.savefig(new_name)
    plt.close(fig)
	
def plot_figs(pitch_l,yaw_l,roll_l,show=1,scatter=0):
	# row and column sharing
	#f = plt.figure(1)
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
	#plt.tight_layout()
	if scatter:
		ax1.scatter(yaw_l, pitch_l)
		ax2.scatter(pitch_l, roll_l)
		ax3.scatter(roll_l, yaw_l, color='r')
	else:
		ax1.plot(yaw_l, pitch_l)
		ax2.plot(pitch_l, roll_l)
		ax3.plot(roll_l, yaw_l, color='r')
	ax1.set_title('pitch = f(yaw)')	
	ax2.set_title('roll = f(pitch)')
	ax3.set_title('yaw = f(roll)')
	if show:
		plt.show()
	return fig

def plot_all(motion,name_dir,save_fig,show,scatter):
	stg = motion + ".orpl"
	list_dir = os.listdir(name_dir)
	l = []
	for name in list_dir:
		if stg in name:
			l += [name]
	for name in l:
		plot_from_file(name,name_dir,save_fig,show,scatter)

def normalize(file_path):
	(pitch_l,yaw_l,roll_l) = get_coord(file_path)
	normalized_pitch = (pitch_l-np.mean(pitch_l))/np.std(pitch_l)
	normalized_yaw= (yaw_l-np.mean(yaw_l))/np.std(yaw_l)
	normalized_roll= (roll_l-np.mean(roll_l))/np.std(roll_l)
	return normalized_pitch,normalized_yaw,normalized_roll

def save_normalized(motion,name_dir):
	stg = motion + ".orpl"
	list_dir = os.listdir(name_dir)
	l = []
	for name in list_dir:
		if stg in name:
			l += [name]

	for name in l:
		(pitch_l,yaw_l,roll_l) = normalize(name_dir+'\\'+name)
		try:
			os.mkdir(name_dir+'\\Normalized')
		except FileExistsError:
			pass
		f = open(name_dir+'\\Normalized\\'+name,'w')
		f.write('yaw pitch roll\n')
		for i in range(len(pitch_l)):
			f.write('{0} {1} {2}\n'.format(yaw_l[i],pitch_l[i],roll_l[i]))
		f.close()
			
motions = ['Roulis','Lacet']
list_dir = next(os.walk('D:\Documents\Projet Long - Oculus Rift\Data'))[1]
list_dir = ['D:\Documents\Projet Long - Oculus Rift\Data\\'+s for s in list_dir]
save_fig = 1 # to save the figure
scatter = 0
show = 0 # to plot the figure
norm = 1 # to normalize data before processing it

for directory in list_dir:
	for motion in motions:
		#save_normalized(motion,directory)
		plot_all(motion,directory,save_fig,show,scatter)
