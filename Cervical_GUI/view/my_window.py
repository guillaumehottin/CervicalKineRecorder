# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QMainWindow

from controller.my_window_controller import MyWindowController
from model.file_manager import create_last_profile_used_file

from view.acquistion_tab import AcquisitionTab
from view.hull_and_spline_tab import HullAndSplinesTab
from view.hulls_tab import HullsTab
from view.new_profile_dialog import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets

from view.wavelet_tab import WaveletTab

APP_ICON                        = "./icone.ico"
LAST_PROFILE_USED_LIST_LIMIT    = 5


class MyWindow(QMainWindow):
    """
    This class is used to define the main window GUI
    Here you can find the menu bar & status bar set up, the tab instanciation and other set up on the window on itself
    """

    def __init__(self, window):
        """
        This function is used to declare and instanciate all class attributes
        :param window: The window in which this GUI will be displayed
        """
        super(MyWindow, self).__init__()

        # WINDOW SETTINGS
        window.setObjectName("Cervical")
        window.resize(814, 590)
        window.setWindowIcon(QtGui.QIcon(APP_ICON))

        # ATTRIBUTES
        self.my_window_controller   = MyWindowController(self)
        self.parent                 = window

        # TAB WIDGET
        self.tabs                   = QtWidgets.QTabWidget(window)
        self.tab_acquisition        = AcquisitionTab(self, self.my_window_controller)
        self.tab_hull_and_splines   = HullAndSplinesTab(self, self.my_window_controller)
        self.tab_hulls              = HullsTab(self, self.my_window_controller)
        self.tab_wavelet            = WaveletTab(self, self.my_window_controller)

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
        self.action_create_model        = QtWidgets.QAction(window)
        self.action_load_model          = QtWidgets.QAction(window)
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
                    self.last_profiles_actions[i].triggered.connect(
                        lambda: self.my_window_controller.load_last_profile_used())
                    self.menu_last_profile.addAction(self.last_profiles_actions[i])

                i += 1
        else:
            self.menu_last_profile.setEnabled(False)

        # Disable all fields in acquisition tab
        self.update_ui(False)
        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to set up the component position and logical
        It fills in the menu bar, create action and link them to handler
        :return: Nothing
        """
        # TABS
        self.tabs.addTab(self.tab_acquisition, "AcquisitionTab")
        self.tabs.addTab(self.tab_hull_and_splines, "Hull and Splines")
        self.tabs.addTab(self.tab_hulls, "Hulls")
        self.tabs.addTab(self.tab_wavelet, "Wavelet")

        # MENUBAR
        self.menubar.setGeometry(QtCore.QRect(0, 0, 814, 21))

        # WINDOW SETTINGS
        self.parent.setCentralWidget(self.tabs)
        self.parent.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        self.parent.setStatusBar(self.statusbar)

        # ACTIONS
        self.action_new_profile.setObjectName("actionNouveau_profil")
        self.action_load_profile.setObjectName("actionCharger_profil")
        self.action_load_curves.setObjectName("actionCharger_courbes")
        self.action_create_model.setObjectName("actionCréerModèle")
        self.action_load_model.setObjectName("actionChargerModèle")
        self.action_documentation.setObjectName("actionDocumentation")

        # ACTION LISTENER
        self.action_new_profile.triggered.connect(self.my_window_controller.new_profile_menu_handler)
        self.action_load_profile.triggered.connect(self.my_window_controller.load_profile_menu_handler)
        self.action_load_curves.triggered.connect(self.my_window_controller.load_curves_menu_handler)
        self.action_create_model.triggered.connect(self.my_window_controller.create_model_handler)
        self.action_load_model.triggered.connect(self.my_window_controller.load_model_handler)
        self.action_documentation.triggered.connect(self.my_window_controller.about_menu_handler)

        # MENU BAR SET UP
        self.menu_profile.addAction(self.action_new_profile)
        self.menu_profile.addAction(self.action_load_profile)
        self.menu_profile.addAction(self.menu_last_profile.menuAction())
        self.menu_curves.addAction(self.action_load_curves)
        self.menu_model.addAction(self.action_create_model)
        self.menu_model.addAction(self.action_load_model)
        self.menu_about.addAction(self.action_documentation)
        self.menubar.addAction(self.menu_profile.menuAction())
        self.menubar.addAction(self.menu_curves.menuAction())
        self.menubar.addAction(self.menu_model.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        self.parent.setWindowTitle(_translate("MyWindow", "Cervical"))

        # MENU
        self.menu_profile.setTitle(_translate("MyWindow", "Profil"))
        self.menu_last_profile.setTitle(_translate("MyWindow", "Profil récent"))
        self.menu_curves.setTitle(_translate("MyWindow", "Courbes"))
        self.menu_model.setTitle(_translate("MyWindow", "Modèle"))
        self.menu_about.setTitle(_translate("MyWindow", "A propos"))
        self.action_new_profile.setText(_translate("MyWindow", "Nouveau profil"))
        self.action_load_profile.setText(_translate("MyWindow", "Charger profil"))
        self.action_load_curves.setText(_translate("MyWindow", "Charger courbes"))
        self.action_create_model.setText(_translate("MyWindow", "Créer modèle"))
        self.action_load_model.setText(_translate("MyWindow", "Charger modèle"))
        self.action_documentation.setText(_translate("MyWindow", "Documentation"))

    def update_ui(self, enable, first_name="Prénom", last_name="Nom", age="XX"):
        """
        This function is used to update the GUI
        It calls update GUI on the acquisition tab and also enable or disable the load curves menu
        :param enable: Boolean used to enable or disable fields
        :param first_name: String containing first name to display
        :param last_name: String containing last name to display
        :param age: String containing age to display
        :return: Nothing
        """

        # REACTIVATE ALL FIELDS AND BUTTONS
        self.tab_acquisition.update_ui(enable, first_name, last_name, age)

        # MENU
        self.action_load_curves.setEnabled(enable)
