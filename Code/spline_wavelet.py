import numpy as np
from scipy import interpolate
import shapely.geometry as geo
import myutils
import matplotlib.pyplot as plt
import plot_serie as pls
import glob
import matplotlib.patches as patches
##############################################
#Consider three angles: Yaw, Pitch and Roll:
#1) Interpolate angles with B-Splines
#2) Build Morlet Wavelets of B-Splibes
# Roll wavelets seems to have more amplitude
# with a pathological person.
#For this, I only consider the central part of the plot.
#It's possible to change the wavelets type.
##############################################


##############################################
#Get data in .orpl file
#Input : _path : String (Location of file)
##############################################
def get_file_data(path):
    f = open(path,"r")
    data = f.readlines()
    yaw_l, pitch_l, roll_l = [],[],[]
    data.pop(0)

    for i in range(0,len(data)):
        elems = data[i].split(" ")
        yaw_l.append(elems[0])
        pitch_l.append(elems[1])
        roll_l.append(elems[2])
    #Convert to float
    if (yaw_l != []):
        yaw_l = list(map(float, yaw_l))
        pitch_l = list(map(float, pitch_l))
        roll_l = list(map(float, roll_l))

    return yaw_l, pitch_l, roll_l
##############################################
#Interpolate temporal series
#Inputs:
#   _Temp -> List of time
#   _List_angle -> List of yaw, pitch or roll
#   _step:int -> Number of points you want
##############################################
def interpolate_angle(temp,list_angle,step=35):
   
    tck, u = interpolate.splprep([temp[::step], list_angle[::step]], s=0.0)
    x_spline, y_spline = interpolate.splev(np.linspace(0, 1, 150), tck)
    return x_spline, y_spline


##############################################
#Plots B-Splines wavelets and angles wavelets.
#I build a rectangle to study the amplitude of
#roll and pitch.
#More over, There are two verticale lines to
#consider the central part.
#To finish, It saves all figures.
##############################################
if __name__ == "__main__":
    #Morlet Wavelet considered but can be changed
    type_wave = 'morl'
    #Path to access all normalized data
    direct = '../gui/guillaume/Normalized'
    #Build list with all files paths
    list_path = glob.glob(direct + '/*.txt')
    #Threshold for the plot
    thres = 0.15
    for i,path in enumerate(list_path):
        y,p,r = get_file_data(path)
        #Interpolate temporal series
        temp = range(len(y))
        yx_spline, yy_spline = interpolate_angle(temp,y)
        px_spline, py_spline = interpolate_angle(temp,p,step=10)
        rx_spline, ry_spline = interpolate_angle(temp,r,step=10)
        #Build morlet wavelets with B-SPlines
        pitch_coef, pitch_freq, yaw_coef, yaw_freq, roll_coef, roll_freq = pls.get_wavelet(py_spline,yy_spline,ry_spline,type_wave)
        #Build morlet wavelets with original series
        p_c,p_f,y_c,y_f,r_c,r_f = pls.get_wavelet(p,y,r,type_wave)
        #Plot
        n1 = len(yaw_coef[0])
        n2 = len(y_c[0])
        #Build a rectangle to see if Roll is out of it
        rec1 = patches.Rectangle((0, -thres), n1, 2*thres,alpha=0.2)
        rec2 = patches.Rectangle((0, -thres), n2, 2*thres,alpha=0.2)
        
        f, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(yaw_coef[0],'r',pitch_coef[0],'b',roll_coef[0],'g')
        #Only consider this area
        ax1.axvline(x=3*n1/10,color='k',linestyle='--')
        ax1.axvline(x=7*n1/10,color='k',linestyle='--')
        ax1.add_patch(rec1)
        ax1.set_title('Spline')
        ax1.set_ylim([-2,2])
        ax2.plot(y_c[0],'r',p_c[0],'b',r_c[0],'g' )
        ax2.axvline(x=3*n2/10,color='k',linestyle='--')
        ax2.axvline(x=7*n2/10,color='k',linestyle='--')
        ax2.add_patch(rec2)
        ax2.set_title('Measure')
        ax2.set_ylim([-2,2])
        plt.savefig(path.replace('Normalized','Plot').replace('.txt','')+'.png')
        plt.close()

