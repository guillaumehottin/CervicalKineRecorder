# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QWidget
from model.socket_server import *
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

INIT_ANGLE      = 70.0
INIT_SPEED      = 25
INIT_NB_RETURN  = 5
INIT_WAIT_TIME = 0.2
LAST_PROFILE_USED_LIST_LIMIT = 5

HOST = "localhost"
PORT = 50007

class Acquisition(QWidget):

    def __init__(self, window):
        super(Acquisition, self).__init__()

        # ATTRIBUTES
        self.parent             = window
        self.selected_movement  = "Lacet"
        self.angle              = INIT_ANGLE
        self.speed              = INIT_SPEED
        self.nb_return          = INIT_NB_RETURN
        self.wait_time          = INIT_WAIT_TIME
        self.curves_on_graph    = []

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
        self.sock_serv = SocketServer()
        self.sock_serv.start(HOST, PORT)

    def setup_ui(self):

        ###################################################################
        #### ACQUISITION TAB
        ###################################################################

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

        # DEACTIVATE ALL FIELD AND BUTTON
        self.text_area_comment.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.text_angle.setEnabled(False)
        self.text_speed.setEnabled(False)
        self.text_nb_return.setEnabled(False)
        self.text_wait_time.setEnabled(False)
        self.startStopButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.emptyGraph.setEnabled(False)

        # BUTTONS LISTENER
        self.startStopButton.clicked.connect(self.start_stop_button_handler)
        self.emptyGraph.clicked.connect(self.empty_graph_button_handler)
        self.saveButton.clicked.connect(self.save_curves_button_handler)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        # SPIN BOX
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

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
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
        self.text_angle.setValue(INIT_ANGLE)
        self.text_speed.setValue(INIT_SPEED)
        self.text_nb_return.setValue(INIT_NB_RETURN)
        self.text_wait_time.setValue(INIT_WAIT_TIME)

        # BUTTONS
        self.startStopButton.setText(_translate("MainWindow", "Lancer acquisition"))
        self.saveButton.setText(_translate("MainWindow", "Enregistrer"))
        self.emptyGraph.setText(_translate("MainWindow", "Vider les graphiques"))

    @pyqtSlot(name="start_stop_button_handler")
    def start_stop_button_handler(self):

        if self.startStopButton.text() == "Lancer acquisition":
            print('START')
            self.selected_movement  = self.comboBox.currentText()
            self.angle              = self.text_angle.text()
            self.speed              = self.text_speed.text()
            self.nb_return          = self.text_nb_return.text()
            self.wait_time         = self.text_wait_time.text()

            CONF = {"sphereSpeed": str(self.speed), "sphereLimitAngle": str(self.angle), "sphereWaitTime": str(self.wait_time),
                    "sphereCountdownTime": "3", "sphereRoundTripNumber": str(self.nb_return),
                    "profileName": "guillaumelethug", "sphereGreenToYellowAngle": "0.1", "sphereYellowToRedAngle": "0.2"}


            print("=== acquisition.py === Acquisition info : \n" +
                    "MOV: " + str(self.comboBox.currentText()) + "\n" +
                    "ANGLE: " + str(self.angle) + "\n" +
                    "SPEED: " + str(self.speed) + "\n" +
                    "NB RETURN: " + str(self.nb_return) + "\n" +
                    "TIME LIMIT: " + str(self.wait_time) + "\n")



            message = build_startAcquisition_message(CONF)

            self.sock_serv.send(message)
            self.sock_serv.close()

            self.sock_serv = SocketServer()
            self.sock_serv.start(HOST, PORT)

            print(self.sock_serv.receive())

            time_to_wait = calculate_time_for_finish(CONF)
            self.send_continue_thread = SendContinue(self.sock_serv, time_to_wait)
            self.send_continue_thread.start()



            # TODO LAUNCH ACQUISITION

            # UPDATE BUTTON START/STOP
            self.startStopButton.setText("Arrêter acquisition")
            self.startStopButton.setStyleSheet("background-color: red; color:white")

        elif self.startStopButton.text() == "Arrêter acquisition":
            print('STOP')
            # TODO STOP ACQUISITION
            self.sock_serv.send("stopAcquisition")
            self.sock_serv.close()
            print("SENT")
            self.sock_serv = SocketServer()
            print("NEW")
            self.sock_serv.start(HOST, PORT)
            print("started")
            print(self.sock_serv.receive())
            self.sock_serv.close()
            self.startStopButton.setText("Lancer acquisition")
            self.startStopButton.setStyleSheet("background-color: green; color:white")
            # self.send_continue_thread.send = False
            self.sock_serv = SocketServer()
            self.sock_serv.start(HOST, PORT)

    @pyqtSlot(name="empty_graph_button_handler")
    def empty_graph_button_handler(self):

        if len(self.curves_on_graph) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Graphiques vide")
            msg.setInformativeText("Aucune courbes n'est affiché actuellement")
            msg.setWindowTitle("Information")
            msg.exec()
        else:
            confirmation_msg = "Etes vous sur de vouloir supprimer des graphiques toutes " \
                               "les courbes affichées ? (" + len(self.curves_on_graph) + " Courbes)"
            reply = QMessageBox.question(self, 'Attention !',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                print("SUPPRESION EN COURS")
                self.clear_graph()

                # Empty attribute
                self.curves_on_graph    = []

            else:
                print("ANNULATION")

    @pyqtSlot(name="save_curves_button_handler")
    def save_curves_button_handler(self):
        print('SAVE CURVES')

        data    = self.yaw_pitch_roll

        self.selected_movement  = self.comboBox.currentText()
        self.angle              = self.text_angle.text()
        self.speed              = self.text_speed.text()
        self.nb_return          = self.text_nb_return.text()
        self.wait_time         = self.text_wait_time.text()

        param   = [self.selected_movement, self.angle, self.speed, self.nb_return, self.wait_time,
                   self.text_area_comment.toPlainText()]

        # Write Data into file with parameters and comment
        create_file_with_curves(self.last_name+"_"+self.first_name+"_"+self.age+"/", data, param)

    def add_comment(self, hour, comment):
        # TODO DOC
        old_content = "" if self.text_area_comment.toPlainText() == "" else self.text_area_comment.toPlainText() + "\n"
        self.text_area_comment.setPlainText(old_content +
                                            hour + ":\n" +
                                            comment)

    def clear_graph(self):
        # TODO DOC
        self.canvas_up_right.clear()
        self.canvas_down_right.clear()
        self.canvas_down_left.clear()

    def update_ui(self, enable, first_name, last_name, age):
        # TODO DOC
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
        self.saveButton.setEnabled(enable)
        self.emptyGraph.setEnabled(enable)

        if enable:
            # BUTTONS
            self.startStopButton.setStyleSheet("background-color: green; color:white")

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
