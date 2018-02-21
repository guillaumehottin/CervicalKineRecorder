# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialog


class NewProfileDialog(object):

    def __init__(self, dialog):
        dialog.setObjectName("NewProfile")
        dialog.resize(400, 300)
        self.parent = dialog
        # BUTTONBOX
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)

        # GRID LAYOUT
        self.gridLayoutWidget = QtWidgets.QWidget(dialog)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        # LABEL
        self.label_last_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.text_last_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.label_first_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.text_first_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.label_age = QtWidgets.QLabel(self.gridLayoutWidget)
        self.text_age = QtWidgets.QLineEdit(self.gridLayoutWidget)

        self.setup_ui()

    def setup_ui(self):
        # BUTTON BOX
        self.buttonBox.setGeometry(QtCore.QRect(10, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # GRID LAYOUT
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 20, 201, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # LABELS + TEXT EDIT
        # Last name
        self.label_last_name.setObjectName("label_last_name")
        self.gridLayout.addWidget(self.label_last_name, 0, 0, 1, 1)
        self.text_last_name.setObjectName("text_last_name")
        self.gridLayout.addWidget(self.text_last_name, 0, 1, 1, 1)

        # First name
        self.label_first_name.setObjectName("label_first_name")
        self.gridLayout.addWidget(self.label_first_name, 1, 0, 1, 1)
        self.text_first_name.setObjectName("text_first_name")
        self.gridLayout.addWidget(self.text_first_name, 1, 1, 1, 1)

        # Age
        self.label_age.setObjectName("label_age")
        self.gridLayout.addWidget(self.label_age, 2, 0, 1, 1)
        self.text_age.setObjectName("text_age")
        self.text_age.setValidator(QIntValidator(1, 99, self.text_age))
        self.gridLayout.addWidget(self.text_age, 2, 1, 1, 1)

        self.retranslate_ui(self.parent)
        self.buttonBox.accepted.connect(self.parent.accept)
        self.buttonBox.rejected.connect(self.parent.reject)
        QtCore.QMetaObject.connectSlotsByName(self.parent)

    def retranslate_ui(self, new_profile):
        _translate = QtCore.QCoreApplication.translate
        new_profile.setWindowTitle(_translate("NewProfile", "Dialog"))
        self.label_last_name.setText(_translate("NewProfile", "Nom"))
        self.label_first_name.setText(_translate("NewProfile", "Prénom"))
        self.label_age.setText(_translate("NewProfile", "Age"))

    def get_first_name(self):
        return self.text_first_name.text()

    def get_last_name(self):
        return self.text_last_name.text()

    def get_age(self):
        return self.text_age.text()

    @pyqtSlot(name="accept_button_handler")
    def accept_button_handler(self):
        print("11111111111111H2HE")

    # static method to create the dialog and return (first_name, last_name, age, accepted)
    @staticmethod
    def get_info(parent=None):
        dialog = QtWidgets.QDialog()
        ui = NewProfileDialog(dialog)
        result = dialog.exec_()
        first_name = ui.get_first_name()
        last_name = ui.get_last_name()
        age = ui.get_age()
        return first_name, last_name, age, result == QDialog.Accepted


