# -*- coding: utf-8 -*-

import os
import ntpath
from datetime import datetime

FILE_EXTENSION                  = ".orpl"
PATH_TO_STORE_FILES             = "./data/"
EXTENSION_HULLS_MODEL           = ".mdlhl"
EXTENSION_HULLS_SPLINES_MODEL   = ".mdlhls"
LAST_PROFILE_USED_FILE_NAME = "last_profile_used.conf"
# DEBUG
DEBUG = True


def get_all_directory_files(directory_path_string):
    """
    Function used to retrieve all files contained in the given directory path and matching the FILE_EXTENSION
    :param directory_path_string: String containing the directory path we have to look
    :return: String list containing each file name we found
    """
    new_path = directory_path_string.replace("\\", "/").strip("\n")
    list_files = os.listdir(new_path)

    i = 0
    # Go through all files and check if the extension is the one we are looking for
    while i < len(list_files):
        _, file_extension = os.path.splitext(list_files[i])
        if file_extension != FILE_EXTENSION:
            list_files.pop(i)
        else:
            i += 1

    DEBUG and print("=== file_manager.py === PATH TO EXPLORE " + str(new_path))
    DEBUG and print("=== file_manager.py === ALL CURVES FILES " + str(list_files))
    return list_files


def get_coord_from_all_directories(list_dir):
    """
    Function used to retrieve coordinates in all files contained in a list of directories which match the
    FILE_EXTENSION
    :param list_dir: String list containing the directories paths we have to look
    :return: float list list containing, for each file, the three coordinates and the corresponding parameters
    :return: int number of files in each directory
    """
    list_coord = []
    nb_files = []
    for folder in list_dir:
        files = [folder + '/' + f for f in get_all_directory_files(folder)]
        nb_files += [len(files)]
        for f in files:
            list_coord += [[get_coord(f), get_param_from_file(f)]]
    return list_coord, nb_files


def get_all_directories():
    """
    Function used to retrieve the list of directories contained in PATH_TO_STORE_FILES
    :return: String list containing the list of directories names found
    """
    path = os.path.abspath(PATH_TO_STORE_FILES)
    list_dir = os.listdir(path)
    i = 0
    # Go through all files and check if it's a directory
    while i < len(list_dir):
        path_joined = os.path.join(path, list_dir[i])
        if not os.path.isdir(path_joined):
            list_dir.pop(i)
        else:
            i += 1

    DEBUG and print("=== file_manager.py === PATH TO EXPLORE " + str(PATH_TO_STORE_FILES))
    DEBUG and print("=== file_manager.py === ALL DIRECTORIES " + str(list_dir))
    return list_dir


def get_file_name_from_absolute_path(absolute_path):
    """
    This function is used to get the file name from a given absolute path
    :param absolute_path: String containing the given absolute path we have to split
    :return: String containing the file name we found
    """
    head, tail = ntpath.split(absolute_path)
    return tail or ntpath.basename(head)


def create_directory(directory_name):
    """
    Function used to create a directory with the given directory name
    :param directory_name: the name of the new directory
    :return:
    """
    try:
        # Get absolute path from directory name
        abs_path = os.path.abspath(PATH_TO_STORE_FILES + directory_name)

        if not os.path.isdir(abs_path):
            os.makedirs(PATH_TO_STORE_FILES + directory_name)
            return os.path.abspath(PATH_TO_STORE_FILES + directory_name)
        else:
            DEBUG and DEBUG and print("==== file_manager.py ==== ERROR: directory already exist")
            raise OSError
    except OSError:
        raise OSError


def get_coord(file_path):
    """
    Function used to parse the file at the given file_path and retrieve the list of values it contains (yaw, pitch roll)
    :param file_path: String, the file path we have to parse
    :return: String list, String list, String list - Three lists containing the yaw pitch rolls values
    """
    # Get list of coordinates in an ORPL file (yaw,pitch_roll)
    f = open(file_path, "r")
    data = f.readlines()
    f.close()
    yaw_l, pitch_l, roll_l = [], [], []

    found = False
    j = 0
    while not found and j < len(data):
        if data[j].strip("\n") == "== VALUES ==":
            found = True
        j += 1

    if not found:
        data_position = data[2:]
    else:
        # Pop data until the list of coord
        # Remove also the header:
        # yaw   pitch   roll
        data_position = data[j+1:]

    for i in range(len(data_position)):
        elems = data_position[i].strip("\n").split(" ")
        yaw_l.append(elems[0])
        pitch_l.append(elems[1])
        roll_l.append(elems[2])

    pitch_l = list(map(float, pitch_l))
    yaw_l   = list(map(float, yaw_l))
    roll_l  = list(map(float, roll_l))

    return yaw_l, pitch_l, roll_l


def create_last_profile_used_file():
    """
    This function is used to create or read the LAST_PROFILE_USED_FILE_NAME file content located in the current
    directory
    If it does not exist yet, we create it otherwise we read it and retrieve info
    :return:
    """
    abs_path = os.path.abspath("./"+LAST_PROFILE_USED_FILE_NAME)
    # If the file does not exist yet, we create it
    if not os.path.isfile(abs_path):
        open("./" + LAST_PROFILE_USED_FILE_NAME, "a").close()
        return []

    else:  # Otherwise we read its content
        with open("./" + LAST_PROFILE_USED_FILE_NAME, "r") as file:
            # We retrieve the list of last profiles used
            list_profiles = file.readlines()
            DEBUG and print("==== file_manager.py ==== PROFILES READ: " + str(list_profiles))

            # We check if each profile still exist in the folder,
            # otherwise we do not return them
            i = 0
            while i < len(list_profiles):
                abs_path_dir = os.path.abspath(PATH_TO_STORE_FILES + list_profiles[i].strip("\n"))
                DEBUG and print("==== file_manager.py ==== CURRENT PATH: " + abs_path_dir)

                # If the directory does not exist anymore we delete the line
                if not os.path.isdir(abs_path_dir):
                    DEBUG and print("==== file_manager.py ==== PROFILE DOES NOT EXIST ANYMORE")
                    list_profiles.pop(i)

                i += 1
            DEBUG and print("==== file_manager.py ==== PROFILES UPDATED: " + str(list_profiles))
            return list_profiles


def add_profile_used(profile_name):
    """
    This function is used to add a profile to the last profile used if it does not appear in it yet
    :param profile_name: String, the profile name we have to add to the file
    :return: Boolean to know whether it has been added or not
    """
    # We open the file in writing mode that was created before
    # And we return all the profiles
    try:
        abs_path = os.path.abspath("./"+LAST_PROFILE_USED_FILE_NAME)
        DEBUG and print("=== file_manager.py === FILE EXISTING ? " + str(os.path.isfile(abs_path)))

        file_read = open(abs_path, "r")
        content = file_read.readlines()
        file_read.close()

        DEBUG and print("==== file_manager.py ==== CONTENT READ: " + str(content))
        # We check if the current profile name is not already in
        # the last profile used
        i = 0
        while i < len(content):
            tmp_comparison = content[i].strip()
            if profile_name == tmp_comparison:
                DEBUG and print("==== file_manager.py ==== I FOUND ANOTHER OCCURENCE OF THE SAME PROFILE")
                # We remove the current element from the list
                content.pop(i)
            i += 1

        DEBUG and print("==== file_manager.py ==== CONTENT UPDATED: " + str(content))

        # Rewrite content to file
        file_write = open(abs_path, "w")
        file_write.seek(0, 0)
        DEBUG and print("=== file_manager.py === PROFILE NAME " + profile_name)
        file_write.write(profile_name + "\n")
        for i in range(0, len(content)):
            file_write.write(content[i])

        file_write.close()
        return True
    except IOError as e:
        DEBUG and print("=== file_manager.py === I/O error profile not added({0}): {1}".format(e.errno, e.strerror))
        return False


def create_file_with_curves(directory, data, param):
    """
    This function is used to create a curve file with its parameters and comments
    :param directory: String, the directory in which we have to create the file
    :param data: [String list, String list, String list], the three list yaw, pitch and roll
    :param param: [String, String, String, String, String, String], selected_movement, max_angle, speed,
            nb_return, wait_time_ comment
    :return: Nothing
    """

    DEBUG and print("=== file_manager.py === WRITE FILE")
    # Get current  time
    now = datetime.now()

    # Extract param
    [movement, angle, speed, nb_return, wait_time, comment] = param

    # Extract data
    [yaw, pitch, roll] = data

    # Create the file name
    file_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" +\
                str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + FILE_EXTENSION

    # Create the file
    try:
        abs_path = os.path.abspath(PATH_TO_STORE_FILES + directory + file_name)
        DEBUG and print("=== file_manager.py === ABSOLUTE PATH " + abs_path)

        with open(abs_path, 'w') as file:

            file.write("== PARAMETERS ==" + "\n")
            file.write("movement:" + movement + "\n")
            file.write("angle:" + str(angle) + "\n")
            file.write("speed:" + str(speed) + "\n")
            file.write("nb_return:" + str(nb_return) + "\n")
            file.write("wait_time:" + str(wait_time) + "\n")

            file.write("== COMMENTS ==" + "\n")
            file.write(comment + "\n")

            file.write("== VALUES ==" + "\n")
            file.write("yaw pitch roll" + "\n")

            for y, p, r in zip(yaw, pitch, roll):
                # WRITE VALUES
                # <yaw> <pitch> <roll>
                file.write(str(y) + " " + str(p) + " " + str(r) + "\n")

            file.close()
            return True
    except IOError as e:
        DEBUG and print("=== file_manager.py === I/O error file not saved({0}): {1}".format(e.errno, e.strerror))
        return False


def get_param_from_file(file_path):
    """
    This function is used to parsed the file at the given file_path and retrieve the param (movement, angle, speed,
    nb_return, wait_time, comments)
    :param file_path: String containing the path of file we have to parse
    :return: [String, String, String, String, String, String]: movement, angle, speed, nb_return, wait_time, comments
    """
    DEBUG and print("=== file_manager.py === FILE PATH " + file_path)
    f = open(file_path, "r")
    data = f.readlines()
    f.close()

    # REMOVE THE FIRST LINE: == PARAMETERS ==
    data.pop(0)

    movement    = data[0].split(":")[1].strip("\n")
    angle       = data[1].split(":")[1].strip("\n")
    speed       = data[2].split(":")[1].strip("\n")
    nb_return   = data[3].split(":")[1].strip("\n")
    wait_time   = data[4].split(":")[1].strip("\n")

    found_comments  = False
    found_values    = False
    index_comments  = -1
    index_values    = -1
    j = 0
    # Retrieve the index of the line '== COMMENTS =='
    while (not (found_comments and found_values)) and j < len(data):
        if data[j].strip("\n") == "== COMMENTS ==":
            found_comments = True
            index_comments = j

        elif data[j].strip("\n") == "== VALUES ==":
            found_values = True
            index_values = j
        j += 1

    comment = ''.join(data[index_comments+1:index_values])
    return movement, angle, speed, nb_return, wait_time, comment

