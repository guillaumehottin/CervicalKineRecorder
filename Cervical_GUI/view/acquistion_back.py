# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextDocument
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QInputDialog, QMessageBox, QWidget
import os

from model.file_manager import create_directory, get_file_name_from_absolute_path, create_file_with_curves, read_file, \
    get_coord, create_last_profile_used_file, add_profile_used, get_param_from_file, get_all_directories
from model.myutils import RGBA_arg
from model.plot_canvas import PlotCanvas

from view.model_generator_dialog import ModelGeneratorDialog
from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from view.curves_dialog import CurvesDialog

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


class Acquisition(QMainWindow):

    def __init__(self, window):
        super(Acquisition, self).__init__()

        # ATTRIBUTES
        self.directory_path     = ""
        self.first_name         = ""
        self.last_name          = ""
        self.age                = ""
        self.curves_on_graph    = []
        self.selected_movement  = "Lacet"
        self.angle              = INIT_ANGLE
        self.speed              = INIT_SPEED
        self.nb_return          = INIT_NB_RETURN
        self.wait_time          = INIT_WAIT_TIME
        self.yaw_pitch_roll     = []

        # TAB WIDGET
        self.tabs               = QtWidgets.QTabWidget(window)
        self.tab_acquisition    = QWidget(self.tabs)
        self.tab_modelization   = QWidget(self.tabs)

        window.setObjectName("Acquisition")
        window.resize(814, 590)
        self.centralwidget      = QtWidgets.QWidget(window)
        self.gridLayoutWidget   = QtWidgets.QWidget(self.centralwidget)

        ###################################################################
        #### ACQUISITION TAB
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

        ###################################################################
        #### MAIN WINDOW TAB
        ###################################################################

        # MENU BAR
        self.menubar            = QtWidgets.QMenuBar(window)
        self.menu_profile       = QtWidgets.QMenu("menuProfil", self.menubar)
        self.menu_last_profile  = QtWidgets.QMenu("menuProfil_récent", self.menu_profile)
        self.menu_curves        = QtWidgets.QMenu("menuCourbes", self.menubar)
        self.menu_model         = QtWidgets.QMenu("menuModel", self.menubar)
        self.menu_about         = QtWidgets.QMenu("menuA_propos", self.menubar)

        # ACTIONS
        self.action_new_profile         = QtWidgets.QAction(window)
        self.action_load_profile        = QtWidgets.QAction(window)
        self.action_load_curves         = QtWidgets.QAction(window)
        self.action_load_files_model    = QtWidgets.QAction(window)
        self.action_documentation       = QtWidgets.QAction(window)

        # STATUS BAR = UNUSED
        self.statusbar = QtWidgets.QStatusBar(window)

        # CREATE THE LAST PROFILE USED FILE IF IT DOES NOT EXIST YET
        self.last_profiles_used = create_last_profile_used_file()
        self.last_profiles_actions = []

        if len(self.last_profiles_used) > 0:

            i = 0
            # Limit 5 old profiles and init actions
            # The shortest list ([0,1,2,3,4,..] or self.last_profile_used)
            # will set the number of loop (ie: if last_profile_used is shorter than 5
            # we will stop before 5)
            for _, item in zip(range(LAST_PROFILE_USED_LIST_LIMIT), self.last_profiles_used):
                # If the current item is not empty
                if item.strip("\n") != "":
                    self.last_profiles_actions.insert(i, QtWidgets.QAction(window))
                    self.last_profiles_actions[i].setObjectName("action_"+item)
                    self.last_profiles_actions[i].setText(item.replace("_", " "))
                    self.last_profiles_actions[i].triggered.connect(self.load_last_profile_used)
                    self.menu_last_profile.addAction(self.last_profiles_actions[i])

                i += 1
        else:
            self.menu_last_profile.setEnabled(False)

        ###################################################################
        #### MODELIZATION TAB
        ###################################################################
        self.grid_layout_modelization = QtWidgets.QGridLayout()
        # CANVAS
        self.canvas_up_left_modelization    = PlotCanvas(self, title="Données temporelles")
        self.canvas_up_right_modelization   = PlotCanvas(self, title="Décomposition en ondelettes")
        self.canvas_down_right_modelization = PlotCanvas(self, title="Spline")
        self.canvas_down_left_modelization  = PlotCanvas(self, title="Enveloppes concaves")

        self.setup_ui(window)

    def setup_ui(self, window):

        # TABS
        self.tabs.addTab(self.tab_acquisition, "Acquisition")
        self.tabs.addTab(self.tab_modelization, "Modélisation")

        ###################################################################
        #### ACQUISITION TAB
        ###################################################################

        # CENTRAL WIDGET ACQUISITION
        self.tab_acquisition.setLayout(self.gridLayout)
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
            # Menu bar
        self.action_load_curves.setEnabled(False)

        # BUTTONS LISTENER
        self.startStopButton.clicked.connect(self.start_stop_button_handler)
        self.emptyGraph.clicked.connect(self.empty_graph_button_handler)
        self.saveButton.clicked.connect(self.save_curves_button_handler)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        window.setCentralWidget(self.tabs)

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

        ###################################################################
        #### MODELIZATION TAB
        ###################################################################
        self.tab_modelization.setLayout(self.grid_layout_modelization)

        self.grid_layout_modelization.addWidget(self.canvas_up_left_modelization, 0, 0)
        self.grid_layout_modelization.addWidget(self.canvas_up_right_modelization, 0, 1)
        self.grid_layout_modelization.addWidget(self.canvas_down_left_modelization, 1, 0)
        self.grid_layout_modelization.addWidget(self.canvas_down_right_modelization, 1, 1)

        ###################################################################
        #### MAIN WINDOW
        ###################################################################

        #### MENUBAR
        self.menubar.setGeometry(QtCore.QRect(0, 0, 814, 21))

        window.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        ## ACTIONS
        self.action_new_profile.setObjectName("actionNouveau_profil")
        self.action_load_profile.setObjectName("actionCharger_profil")
        self.action_load_curves.setObjectName("actionCharger_courbes")
        self.action_load_files_model.setObjectName("actionChargerFichier")
        self.action_documentation.setObjectName("actionDocumentation")

        # ACTION LISTENER
        self.action_new_profile.triggered.connect(self.new_profile_menu_handler)
        self.action_load_profile.triggered.connect(self.load_profile_menu_handler)
        self.action_load_curves.triggered.connect(self.load_curves_menu_handler)
        self.action_load_files_model.triggered.connect(self.load_files_model_handler)
        self.action_documentation.triggered.connect(self.about_menu_handler)

        self.menu_profile.addAction(self.action_new_profile)
        self.menu_profile.addAction(self.action_load_profile)
        self.menu_profile.addAction(self.menu_last_profile.menuAction())
        self.menu_curves.addAction(self.action_load_curves)
        self.menu_model.addAction(self.action_load_files_model)
        self.menu_about.addAction(self.action_documentation)
        self.menubar.addAction(self.menu_profile.menuAction())
        self.menubar.addAction(self.menu_curves.menuAction())
        self.menubar.addAction(self.menu_model.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())

        self.retranslate_ui(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslate_ui(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("MainWindow", "MainWindow"))
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

        # MENU
        self.menu_profile.setTitle(_translate("MainWindow", "Profil"))
        self.menu_last_profile.setTitle(_translate("MainWindow", "Profil récent"))
        self.menu_curves.setTitle(_translate("MainWindow", "Courbes"))
        self.menu_model.setTitle(_translate("MainWindow", "Modèle"))
        self.menu_about.setTitle(_translate("MainWindow", "A propos"))
        self.action_new_profile.setText(_translate("MainWindow", "Nouveau profil"))
        self.action_load_profile.setText(_translate("MainWindow", "Charger profil"))
        self.action_load_curves.setText(_translate("MainWindow", "Charger courbes"))
        self.action_load_files_model.setText(_translate("MainWindow", "Regénérer avec..."))
        self.action_documentation.setText(_translate("MainWindow", "Documentation"))

    @pyqtSlot(name="new_profile_menu_handler")
    def new_profile_menu_handler(self):
        self.first_name, self.last_name, self.age, accepted = NewProfileDialog.get_info()

        if accepted:
            print("=== acquisition.py === User info : \n " +
                    "FIRST NAME " + self.first_name + "\n" +
                    "LAST NAME " + self.last_name + "\n" +
                    "AGE " + self.age)
            try:
                self.directory_path = create_directory(self.last_name.lower() + "_" + self.first_name.lower() +
                                                       "_" + self.age)
                # Update label value
                self.update_ui()

                print("=== acquisition.py === DIRECTORY CREATED AT: " + self.directory_path)

            except OSError:
                print("=== acquisition.py === DIRECTORY ALREADY EXIST AT: " + self.directory_path)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Dossier déjà existant")
                msg.setInformativeText("Le patient que vous avez voulu créé existe déjà, veuillez changer de nom")
                msg.setWindowTitle("Erreur")
                msg.exec()

        else:
            print("=== acquisition.py === OPERATION CANCELED")

    @pyqtSlot(name="load_profile_menu_handler")
    def load_profile_menu_handler(self):
        new_path = str(QFileDialog.getExistingDirectory(self, "Sélectionner un dossier",
                                                        PATH_TO_STORE_FILE , QFileDialog.ShowDirsOnly))

        # If the user canceled
        if not new_path:
            return

        old_directory_name = get_file_name_from_absolute_path(self.directory_path).strip("\n")
        new_directory_name = get_file_name_from_absolute_path(new_path).strip("\n")

        # If the user try to load the same profile as before
        if old_directory_name != new_directory_name:
            self.directory_path = new_path
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Profil inchangé")
            msg.setInformativeText("Le profil que vous avez chargé est déjà chargé dans l'application")
            msg.setWindowTitle("Information")
            msg.exec()
            return

        print("=== acquisition.py === FOLDER LOADED : " + self.directory_path)

        directory_name = get_file_name_from_absolute_path(self.directory_path)

        try:
            [self.last_name, self.first_name, self.age] = directory_name.split("_")

            # Add profile to "last_profile_used" file
            add_profile_used(directory_name)

            self.update_ui()
            self.clear_graph()

            print("=== acquisition.py === User info : \n " +
                  "FIRST NAME " + self.first_name + "\n" +
                  "LAST NAME " + self.last_name + "\n" +
                  "AGE " + self.age)

        except ValueError:
            # DISPLAY POP UP ERROR AND DO NOTHING
            print("=== acquisition.py === INCORRECT FOLDER NAME")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Format de dossier incorrect")
            msg.setInformativeText("Le dossier que vous avez sélectionné ne suit pas la convention qui est : "
                                   "Nom_prénom_age")
            msg.setWindowTitle("Erreur")
            msg.exec()
            return

    @pyqtSlot(name="load_last_profile_used")
    def load_last_profile_used(self):
        sending_button  = self.sender()
        text_button     = sending_button.text()

        try:
            [new_last_name, new_first_name, new_age] = text_button.split(" ")

            if new_last_name == self.last_name and new_first_name == self.first_name and \
                    new_age.strip("\n") == self.age.strip("\n"):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Profil inchangé")
                msg.setInformativeText("Le profil récent que vous avez chargé est déjà chargé dans l'application")
                msg.setWindowTitle("Information")
                msg.exec()
                return
            else:
                [self.last_name, self.first_name, self.age] = [new_last_name, new_first_name, new_age]
                add_profile_used(self.last_name + "_" + self.first_name + "_" + self.age.strip("\n"))
                self.directory_path = os.path.abspath(PATH_TO_STORE_FILE + text_button.replace(" ", "_")).strip("\n")
                self.update_ui()
                self.clear_graph()

        except ValueError:
            # DISPLAY POP UP ERROR AND DO NOTHING
            print("=== acquisition.py === INCORRECT FOLDER NAME")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Format de dossier incorrect")
            msg.setInformativeText("Le profil récent que vous avez sélectionné n'est plus valide... \n"
                                   "Veuillez en créer ou en sélectionner un autre ")
            msg.setWindowTitle("Erreur")
            msg.exec()
        return

    @pyqtSlot(name="load_curves_menu_handler")
    def load_curves_menu_handler(self):
        print('LOAD CURVES' + self.directory_path)
        self.curves_on_graph, accepted = CurvesDialog.get_result(self.directory_path, self.curves_on_graph)

        # The user choose some curves
        if accepted:
            # Empty attributes and graph
            self.yaw_pitch_roll.clear()
            self.clear_graph()
            self.text_area_comment.clear()

            print("=== acquisition.py === selected curves: " + str(self.curves_on_graph))
            for file_name in self.curves_on_graph:
                [yaw_l, pitch_l, roll_l] = get_coord(os.path.join(self.directory_path, file_name))
                self.yaw_pitch_roll.append([yaw_l, pitch_l, roll_l])

                # Pick a random color
                color = RGBA_arg()

                # split the file name
                # EXAMPLE FILE NAME: 13-2-2018_16_11_46.txt
                file_name_splitted = file_name.replace("-", "_").split("_")
                [_, angle, speed, _, _, comment] = get_param_from_file(os.path.join(self.directory_path, file_name))

                #           DAY                             MONTH                       YEAR
                legend = file_name_splitted[0] + "/" + file_name_splitted[1] + "/" + file_name_splitted[2] +\
                         " " + file_name_splitted[3] + "h" + file_name_splitted[4] +\
                         " - " + str(angle) + "° - " + str(speed) + "°/s"

                # LOAD COMMENT
                self.add_comment(legend, comment)

                # PLOT DATA
                self.canvas_up_right.plot(yaw_l, pitch_l, legend=legend, color=color)
                self.canvas_down_right.plot(pitch_l, roll_l, color=color)
                self.canvas_down_left.plot(yaw_l, roll_l, color=color)

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="load_files_model_handler")
    def load_files_model_handler(self):
        print('LOAD FILES' + self.directory_path)
        directories_for_model, accepted = ModelGeneratorDialog.get_result(self.directory_path, self.curves_on_graph)

        # The user choose some directories
        if accepted:
            print("=== acquisition.py === selected directories: " + str(directories_for_model))

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="about_menu_handler")
    def about_menu_handler(self):
        print('ABOUT')

    @pyqtSlot(name="start_stop_button_handler")
    def start_stop_button_handler(self):

        if self.startStopButton.text() == "Lancer acquisition":
            print('START')
            self.selected_movement  = self.comboBox.currentText()
            self.angle              = self.text_angle.text()
            self.speed              = self.text_speed.text()
            self.nb_return          = self.text_nb_return.text()
            self.wait_time         = self.text_wait_time.text()
            print("=== acquisition.py === Acquisition info : \n" +
                    "MOV: " + str(self.comboBox.currentText()) + "\n" +
                    "ANGLE: " + str(self.angle) + "\n" +
                    "SPEED: " + str(self.speed) + "\n" +
                    "NB RETURN: " + str(self.nb_return) + "\n" +
                    "TIME LIMIT: " + str(self.wait_time) + "\n")

            # TODO LAUNCH ACQUISITION

            # UPDATE BUTTON START/STOP
            self.startStopButton.setText("Arrêter acquisition")
            self.startStopButton.setStyleSheet("background-color: red; color:white")

        elif self.startStopButton.text() == "Arrêter acquisition":
            print('STOP')
            # TODO STOP ACQUISITION
            self.startStopButton.setText("Lancer acquisition")
            self.startStopButton.setStyleSheet("background-color: green; color:white")

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
                self.yaw_pitch_roll.clear()
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

    def update_ui(self):
        # TODO DOC
        # UPDATE NAME LABEL
        self.label_nom_prenom.setText(self.first_name.title() + " " + self.last_name.title() + " - " +
                                      self.age.strip("\n") + " ans")

        # FILL IN THE TEXT AREA COMMENT WITH INFO STORED DATA
        self.text_area_comment.clear()

        # REACTIVATE ALL FIELDS AND BUTTONS
        self.text_area_comment.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.text_angle.setEnabled(True)
        self.text_speed.setEnabled(True)
        self.text_nb_return.setEnabled(True)
        self.text_wait_time.setEnabled(True)
        self.startStopButton.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.emptyGraph.setEnabled(True)

        # BUTTONS
        self.startStopButton.setStyleSheet("background-color: green; color:white")

        # MENU
        self.action_load_curves.setEnabled(True)
