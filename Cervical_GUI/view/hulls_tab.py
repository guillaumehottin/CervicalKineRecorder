# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from controller.hull_and_splines_tab_controller import HullAndSplinesTabController
from controller.hulls_tab_controller import HullsTabController
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

DEBUG = False


class HullsTab(QWidget):
    """
    This class is the GUI of the Hulls tab
    Here you can find every aspect of the Widget display (orientation, position, layouts, connection to handler, etc.)
    The logical behind this GUI is located in hulls_tab_controller.py
    """

    def __init__(self, window, my_window_controller):
        """
        This function is used to define and instanciate all class attributes of this class
        :param window: Window in which is displayed this GUI
        """
        super(HullsTab, self).__init__()

        # ATTRIBUTES
        self.hulls_controller       = HullsTabController(self)
        self.my_window_controller   = my_window_controller
        self.parent = window

        # LAYOUTS
        self.grid_layout = QtWidgets.QGridLayout()

        # EXTRA LAYOUTS
        self.left_vertical_layout   = QtWidgets.QVBoxLayout()
        self.right_vertical_layout  = QtWidgets.QVBoxLayout()

        # LABELS
        self.label_pitch    = QtWidgets.QLabel()
        self.label_roll     = QtWidgets.QLabel()
        self.label_healthy  = QtWidgets.QLabel()

        # CANVAS
        self.canvas_left_modeling    = PlotCanvas(self, title="Tangage")
        self.canvas_right_modeling   = PlotCanvas(self, title="Roulis")

        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to manage each widget and component used in this GUI
        Here, layouts are filled in, graph are set up etc.
        :return: Nothing
        """
        # LAYOUTS
        self.setLayout(self.grid_layout)

        # FONT
        font            = QFont("Times", 12, QtGui.QFont.Bold)
        font_healthy    = QFont("Times", 17, QtGui.QFont.Bold)

        # LABELS
        self.label_pitch.setFont(font)
        self.label_pitch.setAlignment(Qt.AlignCenter)
        self.label_pitch.setObjectName("Tangage")

        self.label_roll.setFont(font)
        self.label_roll.setAlignment(Qt.AlignCenter)
        self.label_roll.setObjectName("Roulis")

        self.label_healthy.setFont(font_healthy)
        self.label_healthy.setAlignment(Qt.AlignCenter)
        self.label_healthy.setObjectName("Healthy")

        # EXTRA LAYOUTS
        self.left_vertical_layout.addWidget(self.label_pitch)
        self.left_vertical_layout.addWidget(self.canvas_left_modeling)

        self.right_vertical_layout.addWidget(self.label_roll)
        self.right_vertical_layout.addWidget(self.canvas_right_modeling)

        # GRID LAYOUT
        # Merge the two first columns to center the healthy label
        self.grid_layout.addWidget(self.label_healthy, 0, 0, 1, 2)
        self.grid_layout.addLayout(self.left_vertical_layout, 1, 0)
        self.grid_layout.addLayout(self.right_vertical_layout, 1, 1)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        self.label_healthy.setText(_translate("HullsTab", "Non défini"))

    def clear_graph(self):
        """
        This function is used to empty the three displayed graph and the corresponding parameters
        :return: Nothing
        """
        self.canvas_left_modeling.clear()
        self.canvas_right_modeling.clear()
