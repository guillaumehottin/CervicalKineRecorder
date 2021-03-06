import matplotlib.pyplot as plt
import numpy as np
import os
import myutils
import re

def plot_from_file(name_file,name_dir,save_fig=0,show=1,scatter=0,norm=1):
    """
    Plot the three angular planes given a path to a file containing the data.
    
    Parameters
    ----------
    name_file : str
            The name of the file (not the full path).
    name_dir : str
            The path to the directory which contains the file targeted.
    save_fig : bool
            True to save the figure in the same directory. By default False.
    show : bool
            True to show the figure. By default True.
    scatter : bool
            True to scatter the points instead of plotting lines. By default False.
    norm : bool
            True to use normalized data which must be contained in a subdirectory 
            named 'Normalized'. By default True.
    """
    (pitch_l,yaw_l,roll_l) = myutils.get_coord(name_dir+'/'+name_file)
    fig = plot_figs(pitch_l,yaw_l,roll_l,show,scatter,norm)
    if save_fig:
        if norm:
            full_name = (name_dir+'/Normalized/'+name_file)
        else:
            full_name = (name_dir+'/'+name_file)
        last_dot_index = [m.start() for m in re.finditer('\.',full_name)][-1]
        new_name = full_name[:last_dot_index] + ".png"
        plt.savefig(new_name)
    plt.close(fig)
	
def plot_figs(pitch_l,yaw_l,roll_l,show=1,scatter=0,norm=1):
    """
    Plot the three angular planes given the three angles.
    
    Parameters
    ----------
    pitch_l : list
            The pitch angles.
    roll_l : list
            The roll angles.
    yaw_l : list
            The yaw angles.
    show : bool
            True to show the figure. By default True.
    scatter : bool
            True to scatter the points instead of plotting lines. By default False.
    norm : bool
            True to use normalized data which must be contained in a subdirectory 
            named 'Normalized'. By default True.
            
    Returns
    -------
    figure
            The corresponding figure.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    for ax in [ax1,ax2,ax3]:
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
    if norm:
        (pitch_l,yaw_l,roll_l) = normalize(pitch_l,yaw_l,roll_l)
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

def plot_all(motion,name_dir,save_fig,show,scatter,norm,extension):
    """
    Plot figures using all the matching data available in a given directory.
    
    Parameters
    ----------
    motion : str
            The type of movement: either 'Yaw', 'Pitch' or 'Roll'.
    name_dir : str 
            The (either relative or absolute) path to the directory which contains 
            the data.
    save_fig : bool
            True to save the figure in the same directory. By default False.
    show : bool
            True to show the figure. By default True.
    scatter : bool
            True to scatter the points instead of plotting lines. By default False.
    norm : bool
            True to use normalized data which must be contained in a subdirectory 
            named 'Normalized'. By default True.
    extension : str
            The extension of the data files.
    """
    stg = motion + '.' + extension
    list_dir = os.listdir(name_dir)
    l = []
    for name in list_dir:
        if stg in name:
            l += [name]
    for name in l:
        plot_from_file(name,name_dir,save_fig,show,scatter,norm)
    
    
def save_normalized(motion, name_dir, extension):
    """
    Save the normalized data in a subdirectory named 'Normalized' with the same 
    format as the original data.
    
    Parameters
    ----------
    motion : str
            The type of movement: either 'Yaw', 'Pitch' or 'Roll'.
    name_dir : str 
            The (either relative or absolute) path to the directory which contains 
            the data.
    extension : str
            The extension of the data files.
    """
    stg = motion + '.' + extension
    list_dir = os.listdir(name_dir)
    l = []
    for name in list_dir:
        if stg in name:
            l += [name]

    for name in l:
        (yaw_l, pitch_l, roll_l) = myutils.get_coord(name_dir+'/'+name)
        (yaw_l, pitch_l, roll_l) = normalize(yaw_l, pitch_l, roll_l)
        try:
            os.mkdir(name_dir+'/Normalized')
        except FileExistsError:
            pass
        f = open(name_dir+'/Normalized/'+name,'w')
        f.write('yaw pitch roll\n')
        for i in range(len(pitch_l)):
            f.write('{0} {1} {2}\n'.format(yaw_l[i], pitch_l[i], roll_l[i]))
        f.close()
			
        
if __name__ == '__main__':
    motions = ['']
    dir_name = 'data/'
    list_dir = next(os.walk(dir_name))[1]
    list_dir = [dir_name+s for s in list_dir]
    save_fig = 1 # to save the figure
    scatter = 0
    show = 0 # to plot the figure
    norm = 1 # to normalize data before processing it
    extension = 'orpl'
    
    for directory in list_dir:
    	for motion in motions:
    		save_normalized(motion,directory,extension)
    		#plot_all(motion,directory,save_fig,show,scatter,norm,extension)

# plot_all('Lacet','.',0,1,0)
