# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QWidget
import os

from model.file_manager import create_file_with_curves,\
    get_coord, get_param_from_file
from model.myutils import RGBA_arg
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

PATH_TO_STORE_FILE  = "./data/"
INFO_FILE_EXTENSION          = ".txt"

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class Modelization(QWidget):

    def __init__(self, window):
        super(Modelization, self).__init__()

        self.parent = window

        ###################################################################
        #### MODELIZATION TAB
        ###################################################################
        self.grid_layout_modelization = QtWidgets.QGridLayout()
        # CANVAS
        self.canvas_up_left_modelization = PlotCanvas(self, title="Données temporelles")
        self.canvas_up_right_modelization = PlotCanvas(self, title="Décomposition en ondelettes")
        self.canvas_down_right_modelization = PlotCanvas(self, title="Spline")
        self.canvas_down_left_modelization = PlotCanvas(self, title="Enveloppes concaves")

        self.setup_ui()

    def setup_ui(self):

        ###################################################################
        #### MODELIZATION TAB
        ###################################################################
        self.setLayout(self.grid_layout_modelization)

        self.grid_layout_modelization.addWidget(self.canvas_up_left_modelization, 0, 0)
        self.grid_layout_modelization.addWidget(self.canvas_up_right_modelization, 0, 1)
        self.grid_layout_modelization.addWidget(self.canvas_down_left_modelization, 1, 0)
        self.grid_layout_modelization.addWidget(self.canvas_down_right_modelization, 1, 1)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate


    def clear_graph(self):
        # TODO DOC
        self.canvas_up_right.clear()
        self.canvas_down_right.clear()
        self.canvas_down_left.clear()

    def draw_curves(self, list_curves, directory_path):
        # TODO DOC
        self.clear_graph()
        self.text_area_comment.clear()
        self.curves_on_graph    = list_curves
        yaw_pitch_roll          = []

        print("=== acquisition.py === selected curves: " + str(list_curves))
        for file_name in list_curves:
            [yaw_l, pitch_l, roll_l] = get_coord(os.path.join(directory_path, file_name))
            yaw_pitch_roll.append([yaw_l, pitch_l, roll_l])

            # Pick a random color
            color = RGBA_arg()

            # split the file name
            # EXAMPLE FILE NAME: 13-2-2018_16_11_46.txt
            file_name_splitted = file_name.replace("-", "_").split("_")
            [_, angle, speed, _, _, comment] = get_param_from_file(os.path.join(directory_path, file_name))

            #           YEAR                              MONTH                       DAY
            legend = file_name_splitted[0] + "/" + file_name_splitted[1] + "/" + file_name_splitted[2] + \
                     " " + file_name_splitted[3] + "h" + file_name_splitted[4] + \
                     " - " + str(angle) + "° - " + str(speed) + "°/s"

            # LOAD COMMENT
            self.add_comment(legend, comment)

            # PLOT DATA
            self.canvas_up_right.plot(yaw_l, pitch_l, legend=legend, color=color)
            self.canvas_down_right.plot(pitch_l, roll_l, color=color)
            self.canvas_down_left.plot(yaw_l, roll_l, color=color)
