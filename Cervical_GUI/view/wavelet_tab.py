# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from controller.hull_and_splines_tab_controller import HullAndSplinesTabController
from controller.wavelet_tab_controller import WaveletTabController
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

DEBUG = False


class WaveletTab(QWidget):
    """
    This class is the GUI of the Hull and splines tab
    Here you can find every aspect of the Widget display (orientation, position, layouts, connection to handler, etc.)
    The logical behind this GUI is located in hull_and_splines_tab_controller.py
    """

    def __init__(self, window, my_window_controller):
        """
        This function is used to define and instanciate all class attributes of this class
        :param window: Window in which is displayed this GUI
        """
        super(WaveletTab, self).__init__()

        # ATTRIBUTES
        self.wavelet_tab_controller     = WaveletTabController(self)
        self.my_window_controller       = my_window_controller
        self.parent = window

        # LAYOUTS
        self.grid_layout = QtWidgets.QGridLayout()

        # CANVAS
        self.canvas_up_left_modelization        = PlotCanvas(self, title="Tangage/Tangage moyen")
        self.canvas_up_right_modelization       = PlotCanvas(self, title="Roulis/Roulis moyen")
        self.canvas_down_left_modelization      = PlotCanvas(self, title="Lacet/Lacet moyen")
        self.canvas_down_right_modelization     = PlotCanvas(self, title="Lacet/Roulis/Tangage")

        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to manage each widget and component used in this GUI
        Here, layouts are filled in, graph are set up etc.
        :return: Nothing
        """
        # LAYOUTS
        self.setLayout(self.grid_layout)

        # GRID LAYOUT
        self.grid_layout.addWidget(self.canvas_up_left_modelization, 0, 0)
        self.grid_layout.addWidget(self.canvas_up_right_modelization, 0, 1)
        self.grid_layout.addWidget(self.canvas_down_left_modelization, 1, 0)
        self.grid_layout.addWidget(self.canvas_down_right_modelization, 1, 1)

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
        self.canvas_down_right_modelization.clear()
        self.canvas_down_left_modelization.clear()
        self.canvas_up_right_modelization.clear()
        self.canvas_up_left_modelization.clear()

    def draw_curves(self, list_curves, directory_path):
        pass
