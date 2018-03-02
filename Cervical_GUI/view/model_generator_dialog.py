# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

from model.file_manager import get_all_directories

DEBUG = False


class ModelGeneratorDialog(QDialog):
    """
    This class is used to define the model generator dialog
    Here you can find list view set up, profiles folders retrieval
    """

    def __init__(self, model_generator_dialog, already_selected_profiles):
        """
        This function is used to declare and initialize all class attributes
        :param model_generator_dialog: dialog in which this GUI will be displayed
        :param already_selected_profiles: String list containing the profiles that have been used to generate
                the previous model
        """

        super(ModelGeneratorDialog, self).__init__()

        # DIALOG SETTINGS
        model_generator_dialog.setObjectName("ModelGeneratorDialog")
        model_generator_dialog.resize(550, 450)

        # ATTRIBUTES
        self.parent = model_generator_dialog
        # NOT USED YET
        self.already_selected_model_generator = already_selected_profiles

        # VBOX LAYOUT
        self.vertical_layout = QtWidgets.QVBoxLayout(model_generator_dialog)
        self.horizontal_layout  = QtWidgets.QHBoxLayout(model_generator_dialog)

        # BUTTON BOX
        self.buttonBox = QtWidgets.QDialogButtonBox(model_generator_dialog)

        # SCROLL AREA
        self.scrollArea = QtWidgets.QScrollArea(self.vertical_layout.widget())

        # LIST VIEW
        self.listView = QtWidgets.QListView(self.scrollArea)

        # LABEL
        self.label_model_name = QtWidgets.QLabel()

        # LINE EDIT
        self.text_model_name = QtWidgets.QLineEdit()

        # MODEL
        self.model = QStandardItemModel(self.listView)

        # END SETUP UI
        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to set up all the GUI
        It sets up the scroll area, retrieves the list of profile name and fills in the list view
        :return: Nothing
        """

        # SCROLL AREA
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setEnabled(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # LIST VIEW
        self.listView.setGeometry(QtCore.QRect(0, 0, 530, 450))
        self.listView.setObjectName("listView")

        # ITEMS
        list_directories = get_all_directories()

        # Check if there is some directories to display
        if len(list_directories) > 0:
            DEBUG and print("=== model_generator_dialog.py === LIST DIRECTORIES: " + str(list_directories))
            # DEBUG and print("=== model_generator_dialog.py === ALREADY SELECTED CURVES: " + str(self.already_selected_profiles))
            # GO THROUGH EACH FOLDER FOUND AND PUT IT IN THE LIST VIEW
            for i in range(0, len(list_directories)):
                item = QStandardItem(list_directories[i])
                item.setCheckable(True)
                # if list_directories[i] in self.already_selected_curves:
                #     # Set checkbox checked
                #     item.setCheckState(2)
                self.model.appendRow(item)
        else:  # Display a message that inform the user that there is not any profile at the moment
            item = QStandardItem("Aucune dossier n'est disponible pour le moment")
            item.setCheckable(False)
            self.model.appendRow(item)

        self.listView.setModel(self.model)

        # BUTTON BOX
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton("Regénérer le modèle", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(lambda: self.ok_handler())
        self.buttonBox.rejected.connect(self.parent.reject)

        # LAYOUT
        self.horizontal_layout.addWidget(self.label_model_name)
        self.horizontal_layout.addWidget(self.text_model_name)

        self.vertical_layout.addWidget(self.scrollArea)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.buttonBox)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self):
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        self.parent.setWindowTitle(_translate("Dialog", "Charger des modèles"))
        self.label_model_name.setText(_translate("CurvesDialog", "Nom du modèle : "))

    @pyqtSlot(name="ok_handler")
    def ok_handler(self):
        if self.text_model_name.text() == "":
            color = '#f6989d'  # red
            self.text_model_name.setStyleSheet('QLineEdit { background-color: %s }' % color)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Nom de modèle vide")
            msg.setInformativeText("Vous devez préciser un nom de modèle ")
            msg.setWindowTitle("Erreur")
            msg.exec()
        elif not self.get_selected_directories():
            confirmation_msg = "Aucun patient n'a été sélectionné, aucun modèle de va être généré et les graphiques " \
                               "seront vidés de toute précédent modèle"
            reply = QMessageBox.question(self.parent, 'Attention !',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                print("LA SUPPRESION DES MODELES VA ETRE EFFECTUEE")
                return self.parent.accept()
            else:
                print("ANNULATION")
        else:
            return self.parent.accept()

    def get_selected_directories(self):
        """
        This functin is used to go through all the model and retrieve the selected profiles
        :return: String list containing the selected profiles
        """
        DEBUG and print("=== model_generator_dialog.py === Get selected directories")
        selected_directories = []
        i = 0
        while self.model.item(i):
            if self.model.item(i).checkState():
                selected_directories.append(self.model.item(i).text())
            i += 1

        return selected_directories

    def get_model_name(self):
        return self.text_model_name.text()

    @staticmethod
    def get_result(already_selected_profiles):
        """
        This function is used to create a dialog, fill it with the current UI, execute it and get the result.
        :param already_selected_profiles: String list containing the profiles that have been used to generate
                the previous model
        :return: String list, Boolean - The list of selected profiles names and a boolean which indicates if
        the user has confirm or reject his action
        """
        dialog          = QtWidgets.QDialog()
        ui              = ModelGeneratorDialog(dialog, already_selected_profiles)
        result          = dialog.exec_()
        selected_directories = ui.get_selected_directories()
        model_name      = ui.get_model_name()

        return selected_directories, model_name, result == QDialog.Accepted
