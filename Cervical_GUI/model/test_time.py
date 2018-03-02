from Cervical_GUI.model.plot_time import *

directory = '../tests/'

list_patient = get_list_patient(directory)
list_data = get_list_data(list_patient)

movement, angle, speed, nb_return, wait_time, comment = get_param_from_file(list_data[0])

# mean_pitch, mean_yaw, mean_roll = get_time_mean(list_patient, movement, angle, speed, nb_return, wait_time)

# plot_data(mean_pitch, mean_yaw, mean_roll)


list_param = [movement, angle, speed, nb_return, wait_time, comment]

plot_final_time(list_data[0], list_patient, list_param)