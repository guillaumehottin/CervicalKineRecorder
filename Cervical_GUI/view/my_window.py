# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QInputDialog, QMessageBox, QWidget, QVBoxLayout
import os

from model.file_manager import create_directory, get_file_name_from_absolute_path, \
    create_last_profile_used_file, add_profile_used

from view.acquistion import Acquisition
from view.model_generator_dialog import ModelGeneratorDialog
from view.modelization import Modelization
from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from view.curves_dialog import CurvesDialog
import webbrowser

PATH_TO_STORE_FILE      = "./data/"
INFO_FILE_EXTENSION     = ".txt"
GIT_LINK                = "https://github.com/guillaumehottin/projetlong"
APP_ICON                = "./icone.ico"

INIT_ANGLE      = 70.0
INIT_SPEED      = 25
INIT_NB_RETURN  = 5
INIT_WAIT_TIME = 0.2
LAST_PROFILE_USED_LIST_LIMIT = 5


class MyWindow(QMainWindow):

    def __init__(self, window):
        super(MyWindow, self).__init__()

        # ATTRIBUTES
        self.directory_path     = ""
        self.first_name         = "Prénom"
        self.last_name          = "Nom"
        self.age                = "âge"
        self.curves_on_graph    = []
        self.selected_movement  = "Lacet"
        self.angle              = INIT_ANGLE
        self.speed              = INIT_SPEED
        self.nb_return          = INIT_NB_RETURN
        self.wait_time          = INIT_WAIT_TIME
        self.yaw_pitch_roll     = []

        ###################################################################
        #### MAIN WINDOW
        ###################################################################

        # TAB WIDGET
        self.tabs               = QtWidgets.QTabWidget(window)
        self.tab_acquisition    = Acquisition(self.tabs)
        self.tab_modelization   = Modelization(self.tabs)

        window.setObjectName("Cervical")
        window.resize(814, 590)
        window.setWindowIcon(QtGui.QIcon(APP_ICON))

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
        self.last_profiles_used     = create_last_profile_used_file()
        self.last_profiles_actions  = []

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

        # Disable all fields in acquisition tab
        self.update_ui(False)
        self.setup_ui(window)

    def setup_ui(self, window):

        # TABS
        self.tabs.addTab(self.tab_acquisition, "Acquisition")
        self.tabs.addTab(self.tab_modelization, "Modélisation")
        window.setCentralWidget(self.tabs)

        ###################################################################
        #### ACQUISITION TAB
        ###################################################################

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
        window.setWindowTitle(_translate("MainWindow", "Cervical"))

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
                self.update_ui(True)

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

            self.update_ui(True)

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
                print("TEST 2")
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
                self.update_ui(True)

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
            self.yaw_pitch_roll = []
            self.yaw_pitch_roll = self.tab_acquisition.draw_curves(self.curves_on_graph, self.directory_path)

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
        webbrowser.open(GIT_LINK, new=2)

    def update_ui(self, enable):
        # TODO DOC

        # REACTIVATE ALL FIELDS AND BUTTONS
        self.tab_acquisition.update_ui(enable, self.first_name, self.last_name, self.age)

        # MENU
        self.action_load_curves.setEnabled(enable)
