# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from controller.hull_and_splines_tab_controller import HullAndSplinesTabController
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

DEBUG = False


class HullAndSplinesTab(QWidget):
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
        super(HullAndSplinesTab, self).__init__()

        # ATTRIBUTES
        self.hulls_and_splines_controller    = HullAndSplinesTabController(self)
        self.my_window_controller       = my_window_controller
        self.parent = window

        # LAYOUTS
        self.grid_layout = QtWidgets.QGridLayout()

        # EXTRA LAYOUTS
        self.left_vertical_layout           = QtWidgets.QVBoxLayout()
        self.left_horizontal_rate_layout    = QtWidgets.QHBoxLayout()
        self.left_horizontal_score_layout   = QtWidgets.QHBoxLayout()

        self.right_vertical_layout          = QtWidgets.QVBoxLayout()
        self.right_horizontal_rate_layout   = QtWidgets.QHBoxLayout()
        self.right_horizontal_score_layout  = QtWidgets.QHBoxLayout()

        # LABELS
        self.label_pitch                    = QtWidgets.QLabel()
        self.label_left_rate                = QtWidgets.QLabel()
        self.label_left_rate_value          = QtWidgets.QLabel()
        self.label_left_variability         = QtWidgets.QLabel()
        self.label_left_variability_score   = QtWidgets.QLabel()
        self.label_roll                     = QtWidgets.QLabel()
        self.label_right_rate               = QtWidgets.QLabel()
        self.label_right_rate_value         = QtWidgets.QLabel()
        self.label_right_variability        = QtWidgets.QLabel()
        self.label_right_variability_score  = QtWidgets.QLabel()

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
        new_font = QFont("Times", 12, QtGui.QFont.Bold)

        # LABELS
        # LEFT SIDE
        self.label_pitch.setFont(new_font)
        self.label_pitch.setAlignment(Qt.AlignCenter)

        # RIGHT SIDE
        self.label_roll.setFont(new_font)
        self.label_roll.setAlignment(Qt.AlignCenter)

        # EXTRA LAYOUTS
        # LEFT SIDE
        self.left_horizontal_rate_layout.addWidget(self.label_left_rate)
        self.left_horizontal_rate_layout.addWidget(self.label_left_rate_value)
        self.left_horizontal_score_layout.addWidget(self.label_left_variability)
        self.left_horizontal_score_layout.addWidget(self.label_left_variability_score)

        self.left_vertical_layout.addWidget(self.label_pitch)
        self.left_vertical_layout.addLayout(self.left_horizontal_rate_layout)
        self.left_vertical_layout.addLayout(self.left_horizontal_score_layout)
        self.left_vertical_layout.addWidget(self.canvas_left_modeling)

        # RIGHT SIDE
        self.right_horizontal_rate_layout.addWidget(self.label_right_rate)
        self.right_horizontal_rate_layout.addWidget(self.label_right_rate_value)
        self.right_horizontal_score_layout.addWidget(self.label_right_variability)
        self.right_horizontal_score_layout.addWidget(self.label_right_variability_score)

        self.right_vertical_layout.addWidget(self.label_roll)
        self.right_vertical_layout.addLayout(self.right_horizontal_rate_layout)
        self.right_vertical_layout.addLayout(self.right_horizontal_score_layout)
        self.right_vertical_layout.addWidget(self.canvas_right_modeling)

        # GRID LAYOUT
        self.grid_layout.addLayout(self.left_vertical_layout, 0, 0)
        self.grid_layout.addLayout(self.right_vertical_layout, 0, 1)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        # LEFT SIDE
        self.label_pitch.setText(_translate("MainWindow", "Tangage"))
        self.label_left_variability_score.setText(_translate("MainWindow", "0"))
        self.label_left_variability.setText(_translate("MainWindow", "Variabilité"))
        self.label_left_rate_value.setText(_translate("MainWindow", "0%"))
        self.label_left_rate.setText(_translate("MainWindow", "Taux de points en dehors de l'enveloppe : "))

        # RIGHT SIDE
        self.label_right_variability_score.setText(_translate("MainWindow", "0"))
        self.label_right_variability.setText(_translate("MainWindow", "Variabilité"))
        self.label_right_rate.setText(_translate("MainWindow", "Taux de points en dehors de l'enveloppe : "))
        self.label_right_rate_value.setText(_translate("MainWindow", "0%"))
        self.label_roll.setText(_translate("MainWindow", "Roulis"))

    def clear_graph(self):
        """
        This function is used to empty the three displayed graph and the corresponding parameters
        :return: Nothing
        """
        self.canvas_left_modeling.clear()
        self.canvas_right_modeling.clear()
        self.label_right_rate_value.setText("0%")
        self.label_right_variability_score.setText("0")

    def draw_curves(self, list_curves, directory_path):
        pass
