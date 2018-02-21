# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from controller.modelization_controller import ModelizationController
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

DEBUG = False


class Modelization(QWidget):
    """
    This class is the GUI of the modelization tabs
    Here you can find every aspect of the Widget display (orientation, position, layouts, connection to handler, etc.)
    The logical behind this GUI is located in modelization_controller.py
    """

    def __init__(self, window):
        """
        This function is used to define and instanciate all class attributes of this class
        :param window: Window in which is displayed this GUI
        """
        super(Modelization, self).__init__()

        # ATTRIBUTES
        self.modelization_controller = ModelizationController(self)
        self.parent = window

        # LAYOUTS
        self.grid_layout_modelization = QtWidgets.QGridLayout()

        # CANVAS
        self.canvas_up_left_modelization = PlotCanvas(self, title="Données temporelles")
        self.canvas_up_right_modelization = PlotCanvas(self, title="Décomposition en ondelettes")
        self.canvas_down_right_modelization = PlotCanvas(self, title="Spline")
        self.canvas_down_left_modelization = PlotCanvas(self, title="Enveloppes concaves")

        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to manage each widget and component used in this GUI
        Here, layouts are filled in, graph are set up etc.
        :return: Nothing
        """
        # LAYOUTS
        self.setLayout(self.grid_layout_modelization)

        # GRIDLAYOUT
        self.grid_layout_modelization.addWidget(self.canvas_up_left_modelization, 0, 0)
        self.grid_layout_modelization.addWidget(self.canvas_up_right_modelization, 0, 1)
        self.grid_layout_modelization.addWidget(self.canvas_down_left_modelization, 1, 0)
        self.grid_layout_modelization.addWidget(self.canvas_down_right_modelization, 1, 1)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate

    def clear_graph(self):
        """
        This function is used to empty the three displayed graph and the corresponding parameters
        :return: Nothing
        """
        self.canvas_up_right.clear()
        self.canvas_down_right.clear()
        self.canvas_down_left.clear()

    def draw_curves(self, list_curves, directory_path):
        pass
        # TODO DOC
        # self.clear_graph()
        # self.text_area_comment.clear()
        # self.curves_on_graph    = list_curves
        # yaw_pitch_roll          = []
        #
        # print("=== acquisition.py === selected curves: " + str(list_curves))
        # for file_name in list_curves:
        #     [yaw_l, pitch_l, roll_l] = get_coord(os.path.join(directory_path, file_name))
        #     yaw_pitch_roll.append([yaw_l, pitch_l, roll_l])
        #
        #     # Pick a random color
        #     color = RGBA_arg()
        #
        #     # split the file name
        #     # EXAMPLE FILE NAME: 13-2-2018_16_11_46.txt
        #     file_name_splitted = file_name.replace("-", "_").split("_")
        #     [_, angle, speed, _, _, comment] = get_param_from_file(os.path.join(directory_path, file_name))
        #
        #     #           YEAR                              MONTH                       DAY
        #     legend = file_name_splitted[0] + "/" + file_name_splitted[1] + "/" + file_name_splitted[2] + \
        #              " " + file_name_splitted[3] + "h" + file_name_splitted[4] + \
        #              " - " + str(angle) + "° - " + str(speed) + "°/s"
        #
        #     # LOAD COMMENT
        #     self.add_comment(legend, comment)
        #
        #     # PLOT DATA
        #     self.canvas_up_right.plot(yaw_l, pitch_l, legend=legend, color=color)
        #     self.canvas_down_right.plot(pitch_l, roll_l, color=color)
        #     self.canvas_down_left.plot(yaw_l, roll_l, color=color)
