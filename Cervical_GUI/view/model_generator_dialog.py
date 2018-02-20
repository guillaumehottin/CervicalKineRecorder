# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QSizePolicy, QDialogButtonBox

from model.file_manager import get_all_directory_files, get_all_directories


class ModelGeneratorDialog(object):

    def __init__(self, model_generator_dialog, already_selected_curves):
        model_generator_dialog.setObjectName("ModelGeneratorDialog")
        model_generator_dialog.resize(550, 450)

        # ATTRIBUTES
        # self.already_selected_model_generator = already_selected_curves

        # VBOX LAYOUT
        self.vertical_layout = QtWidgets.QVBoxLayout(model_generator_dialog)

        # BUTTON BOX
        self.buttonBox = QtWidgets.QDialogButtonBox(model_generator_dialog)

        # SCROLL AREA
        self.scrollArea = QtWidgets.QScrollArea(self.vertical_layout.widget())

        # LIST VIEW
        self.listView = QtWidgets.QListView(self.scrollArea)

        # MODEL
        self.model = QStandardItemModel(self.listView)

        # END SETUP UI
        self.setup_ui(model_generator_dialog)

    def setup_ui(self, curve_dialog):

        # SCROLL AREA
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setEnabled(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.vertical_layout.addWidget(self.scrollArea)

        # LIST VIEW
        self.listView.setGeometry(QtCore.QRect(0, 0, 530, 450))
        self.listView.setObjectName("listView")

        # ITEMS
        list_directories = get_all_directories()

        if len(list_directories) > 0:
            print("LIST DIRECTORIES: " + str(list_directories))
            # print("ALREADY SELECTED CURVES: " + str(self.already_selected_curves))
            for i in range(0, len(list_directories)):
                item = QStandardItem(list_directories[i])
                item.setCheckable(True)
                # if list_directories[i] in self.already_selected_curves:
                #     # Set checkbox checked
                #     item.setCheckState(2)
                self.model.appendRow(item)
        else:
            item = QStandardItem("Aucune dossier n'est disponible pour le moment")
            item.setCheckable(False)
            self.model.appendRow(item)

        self.listView.setModel(self.model)

        # BUTTON BOX
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton("Regénérer le modèle", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)

        # self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(curve_dialog.accept)
        self.buttonBox.rejected.connect(curve_dialog.reject)
        self.vertical_layout.addWidget(self.buttonBox)

        self.retranslate_ui(curve_dialog)
        QtCore.QMetaObject.connectSlotsByName(curve_dialog)

    def retranslate_ui(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("Dialog", "Charger des modèles"))

    def get_selected_directories(self):
        print("=== model_generator_dialog.py === Get selected directories")
        selected_directories = []
        i = 0
        while self.model.item(i):
            if self.model.item(i).checkState():
                selected_directories.append(self.model.item(i).text())
            i += 1

        return selected_directories

    # static method to create the dialog and return (first_name, last_name, age, accepted)
    @staticmethod
    def get_result(already_selected_curves, parent=None):
        dialog          = QtWidgets.QDialog()
        ui              = ModelGeneratorDialog(dialog, already_selected_curves)
        result          = dialog.exec_()
        selected_directories = ui.get_selected_directories()

        return selected_directories, result == QDialog.Accepted
