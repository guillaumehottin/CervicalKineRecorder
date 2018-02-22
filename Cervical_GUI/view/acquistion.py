# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from controller.acquisition_controller import AcquisitionController
import os

from model.file_manager import get_coord, get_param_from_file
from model.myutils import RGBA_arg
from model.plot_canvas import PlotCanvas

from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets


DEBUG               = False

#TODO CHANGE CONST LOCATION TO CONTROLLER
HOST = "localhost"
PORT = 50007


class Acquisition(QWidget):
    """
    This class is the GUI of the acquisition tabs
    Here you can find every aspect of the Widget display (orientation, position, layouts, connection to handler, etc.)
    The logical behind this GUI is located in acquisition_controller.py
    """

    def __init__(self, window):
        """
        This function is used to define and instanciate all class attributes of this class
        :param window: Window in which is displayed this GUI
        """
        super(Acquisition, self).__init__()

        # ATTRIBUTES
        self.parent                 = window
        self.acquisition_controller = AcquisitionController(self)

        self.parent.setObjectName("Acquisition")
        self.centralwidget      = QtWidgets.QWidget(self.parent)
        self.gridLayoutWidget   = QtWidgets.QWidget(self.centralwidget)

        self.sock_serv = None

        ###################################################################
        # ACQUISITION TAB
        ###################################################################
        self.gridLayout         = QtWidgets.QGridLayout()

        # CANVAS
        self.canvas_up_right    = PlotCanvas(self, title="Flex-Ext/Rotation")
        self.canvas_down_right  = PlotCanvas(self, title="Incli-Lat/Flex-Ext")
        self.canvas_down_left   = PlotCanvas(self, title="Incli-Lat/Rotation")

        # LAYOUTS
        self.verticalLayout                 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_nom_prenom    = QtWidgets.QHBoxLayout()
        self.horizontalLayout_mvt           = QtWidgets.QHBoxLayout()
        self.horizontalLayout_angle         = QtWidgets.QHBoxLayout()
        self.horizontalLayout_speed         = QtWidgets.QHBoxLayout()
        self.horizontalLayout_return        = QtWidgets.QHBoxLayout()
        self.horizontalLayout_wait_time    = QtWidgets.QHBoxLayout()
        self.horizontalLayout_start_save    = QtWidgets.QHBoxLayout()
        self.horizontalLayout_empty_graph = QtWidgets.QHBoxLayout()

        # LABEL
        self.label_nom_prenom   = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_comment      = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_mvt_selected = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_angle        = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_speed        = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_nb_return    = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_wait_time    = QtWidgets.QLabel(self.gridLayoutWidget)

        # PLAINTEXTEDIT
        self.text_area_comment       = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)

        # LINE EDIT
        self.text_angle         = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.text_speed         = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.text_nb_return     = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.text_wait_time     = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)

        # COMBOBOX
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.available_movements = [
            "Lacet",
            "Roulis",
            "Tangage",
        ]
        self.comboBox.addItems(self.available_movements)

        # BUTTONS
        self.startStopButton    = QtWidgets.QPushButton("startStopButton", self.gridLayoutWidget)
        self.saveButton         = QtWidgets.QPushButton("saveButton", self.gridLayoutWidget)
        self.emptyGraph         = QtWidgets.QPushButton("emptyGraph", self.gridLayoutWidget)

        self.setup_ui()
        # self.sock_serv = SocketServer()
        # self.sock_serv.start(HOST, PORT)

    def setup_ui(self):
        """
        This function is used to manage each widget and component used in this GUI
        Here, layouts are filled in, buttons are set up, etc.
        :return: Nothing
        """

        # CENTRAL WIDGET ACQUISITION
        self.setLayout(self.gridLayout)
        self.centralwidget.setObjectName("centralwidget")

        # BIG GRID LAYOUT & ITS WIDGET
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")

        # CANVAS SETUP
        self.gridLayout.addWidget(self.canvas_up_right, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.canvas_down_right, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.canvas_down_left, 1, 0, 1, 1)

        # LAYOUTS
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 25, 25)
        self.horizontalLayout_nom_prenom.setObjectName("horizontalLayout_nom_prenom")
        self.horizontalLayout_mvt.setObjectName("horizontalLayout__mvt")
        self.horizontalLayout_empty_graph.setObjectName("horizontalLayout_empty_graph²")

        self.verticalLayout.addLayout(self.horizontalLayout_nom_prenom)
        self.verticalLayout.addWidget(self.label_comment)
        self.verticalLayout.addWidget(self.text_area_comment)
        self.verticalLayout.addLayout(self.horizontalLayout_mvt)
        self.verticalLayout.addLayout(self.horizontalLayout_angle)
        self.verticalLayout.addLayout(self.horizontalLayout_speed)
        self.verticalLayout.addLayout(self.horizontalLayout_return)
        self.verticalLayout.addLayout(self.horizontalLayout_wait_time)
        self.verticalLayout.addLayout(self.horizontalLayout_start_save)
        self.verticalLayout.addLayout(self.horizontalLayout_empty_graph)

        # NAME
        self.horizontalLayout_nom_prenom.addWidget(self.label_nom_prenom)

        # PLAIN TEXT EDIT
        self.text_area_comment.canPaste()

        # MOVEMENT
        self.horizontalLayout_mvt.addWidget(self.label_mvt_selected)
        self.horizontalLayout_mvt.addWidget(self.comboBox)

        # ANGLE
        self.horizontalLayout_angle.addWidget(self.label_angle)
        self.horizontalLayout_angle.addWidget(self.text_angle)

        # SPEED
        self.horizontalLayout_speed.addWidget(self.label_speed)
        self.horizontalLayout_speed.addWidget(self.text_speed)

        # RETURN
        self.horizontalLayout_return.addWidget(self.label_nb_return)
        self.horizontalLayout_return.addWidget(self.text_nb_return)

        # TIME LIMIT
        self.horizontalLayout_wait_time.addWidget(self.label_wait_time)
        self.horizontalLayout_wait_time.addWidget(self.text_wait_time)

        # START/STOP + SAVE
        self.horizontalLayout_start_save.addWidget(self.startStopButton)
        self.horizontalLayout_start_save.addWidget(self.saveButton)
        self.horizontalLayout_start_save.setObjectName("horizontalLayout_start_save")

        # EMPTY
        self.horizontalLayout_empty_graph.addWidget(self.emptyGraph)

        # FONT
        new_font = QFont("Times", 12, QtGui.QFont.Bold)

        # LABELS
        self.label_nom_prenom.setFont(new_font)
        self.label_nom_prenom.setAlignment(Qt.AlignCenter)
        self.label_nom_prenom.setObjectName("label_nom_prenom")
        self.label_comment.setObjectName("label_comment")
        self.label_mvt_selected.setObjectName("label_mvt_selected")

        # COMBO BOX
        self.comboBox.setObjectName("comboBox")

        # BUTTONS LISTENER
        self.startStopButton.clicked.connect(self.acquisition_controller.start_stop_button_handler)
        self.emptyGraph.clicked.connect(self.acquisition_controller.empty_graph_button_handler)
        self.saveButton.clicked.connect(self.acquisition_controller.save_curves_button_handler)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        # SPIN BOXES
        self.text_angle.setMinimum(0.5)
        self.text_angle.setMaximum(90)
        self.text_angle.setSingleStep(1)

        self.text_speed.setMinimum(0.5)
        self.text_speed.setMaximum(90)
        self.text_speed.setSingleStep(0.1)

        self.text_nb_return.setMinimum(1)
        self.text_nb_return.setMaximum(50)
        self.text_nb_return.setSingleStep(1)

        self.text_wait_time.setMinimum(0.05)
        self.text_wait_time.setMaximum(10)
        self.text_wait_time.setSingleStep(0.05)

        # Disable save button independently
        self.saveButton.setEnabled(False)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        # LABELS
        self.label_nom_prenom.setText(_translate("MainWindow", "Nom prénom age"))
        self.label_comment.setText(_translate("MainWindow", "Commentaires d'acquisition"))
        self.label_mvt_selected.setText(_translate("MainWindow", "Mouvement sélectionné"))
        self.label_angle.setText(_translate("MainWindow", "Amplitude maximum (en °)"))
        self.label_speed.setText(_translate("MainWindow", "Vitesse de rotation (en °/s)"))
        self.label_nb_return.setText(_translate("MainWindow", "Nombre d'aller retour "))
        self.label_wait_time.setText(_translate("MainWindow", "Temps d'arrêt entre chaque aller retour"))

        # SPINBOX
        self.text_angle.setValue(self.acquisition_controller.INIT_ANGLE)
        self.text_speed.setValue(self.acquisition_controller.INIT_SPEED)
        self.text_nb_return.setValue(self.acquisition_controller.INIT_NB_RETURN)
        self.text_wait_time.setValue(self.acquisition_controller.INIT_WAIT_TIME)

        # BUTTONS
        self.startStopButton.setText(_translate("MainWindow", "Lancer acquisition"))
        self.saveButton.setText(_translate("MainWindow", "Enregistrer"))
        self.emptyGraph.setText(_translate("MainWindow", "Vider les graphiques"))

    def add_comment(self, hour_parameters, comments):
        """
        This function is used to fill in the comment text area with new comments.
        If the area was not empty before, we append the content given
        Otherwise we clear it and we put the given comments in it
        We put comments like this:
            hour & parameters :
            Comment
        :param hour_parameters: A string which will be the title of the comment
                (normally DAY/MONTH/YEAR HH:MM:SS - Max_angle° - speed°/s
        :param comments: string containing the comments we have to display
        :return: Nothing
        """
        old_content = "" if self.text_area_comment.toPlainText() == "" else self.text_area_comment.toPlainText() + "\n"
        self.text_area_comment.setPlainText(old_content +
                                            hour_parameters + ":\n" +
                                            comments)

    def clear_graph(self):
        """
        This function is used to empty the three displayed graph and the corresponding parameters
        :return: Nothing
        """
        self.acquisition_controller.curves_on_graph = []
        self.acquisition_controller.yaw_pitch_roll  = []
        self.canvas_up_right.clear()
        self.canvas_down_right.clear()
        self.canvas_down_left.clear()

    def update_ui(self, enable, first_name, last_name, age):
        """
        This function is used to enable or disable the displayed fields and to set the principal label
        to the given first name, last name and age
        It also clear the comment area, clear the graph and set the start button background to green
        :param enable: Boolean used to enable or disable GUI fields
        :param first_name: First name to display
        :param last_name: Last name to display
        :param age: Age to display
        :return: Nothing
        """
        # UPDATE NAME LABEL
        self.label_nom_prenom.setText(first_name.title() + " " + last_name.title() + " - " +
                                      age.strip("\n") + " ans")

        # FILL IN THE TEXT AREA COMMENT WITH INFO STORED DATA
        self.text_area_comment.clear()

        # GRAPH
        self.clear_graph()

        # REACTIVATE ALL FIELDS AND BUTTONS
        self.text_area_comment.setEnabled(enable)
        self.comboBox.setEnabled(enable)
        self.text_angle.setEnabled(enable)
        self.text_speed.setEnabled(enable)
        self.text_nb_return.setEnabled(enable)
        self.text_wait_time.setEnabled(enable)
        self.startStopButton.setEnabled(enable)
        self.emptyGraph.setEnabled(enable)

        if enable:
            # BUTTONS
            self.startStopButton.setStyleSheet("background-color: green; color:white")

    def draw_curves(self, list_curves, directory_path):
        """
        This function is used to draw on the graph the curves given as parameters
        It clear the comment area, clear the graph, go through each curves name and
        for each it retrieve its values (yaw, pitch, roll) from the file in the directory_path and display it
        on the three graph
        :param list_curves: List of string containing the curves name to draw on the graph
        :param directory_path: String containing the path where we have to look for the given curves names
        :return: Nothing
        """
        self.clear_graph()
        self.text_area_comment.clear()
        self.acquisition_controller.curves_on_graph     = list_curves
        self.acquisition_controller.yaw_pitch_roll      = []
        yaw_pitch_roll          = []

        DEBUG and print("=== acquisition.py === selected curves: " + str(list_curves))
        for file_name in list_curves:
            [yaw_l, pitch_l, roll_l] = get_coord(os.path.join(directory_path, file_name))
            yaw_pitch_roll.append([yaw_l, pitch_l, roll_l])

            # Pick a random color
            color = RGBA_arg()

            # If the curve we are going to draw is the curve given by the Unity app
            if file_name == self.acquisition_controller.TMP_FILE_PATH :
                legend = "Dernière acquisition"
            else:
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

        # Update controller attribute
        self.acquisition_controller.yaw_pitch_roll = yaw_pitch_roll

    def get_curves_on_graph(self):
        """
        This function returns the list of curves names currently displayed on the graph
        :return: List of String containing curves names
        """
        return self.acquisition_controller.curves_on_graph
