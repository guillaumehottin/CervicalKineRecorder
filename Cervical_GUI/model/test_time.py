from Code.plot_time import *
from Code.plot_serie import *
directory = '../tests/'

list_patient = get_list_patient(directory)
list_data = get_list_data(list_patient)

movement, angle, speed, nb_return, wait_time, comment = get_param_from_file(list_data[0])

mean_pitch, mean_yaw, mean_roll = get_time_mean(list_patient, movement, angle, speed, nb_return, wait_time)

plot_data(mean_pitch, mean_yaw, mean_roll)
