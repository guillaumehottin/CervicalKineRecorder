# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialog


class NewProfileDialog(QDialog):
    """
    This class is used to define the new profile dialog GUI
    Here you can find the Text edit and buttons set up
    """

    def __init__(self, dialog):
        """
        This function is used to declare and initialize all class attributes
        :param dialog: The dialog in which this GUI will be displayed
        """

        super(NewProfileDialog, self).__init__()

        # ATTRIBUTES
        self.parent = dialog

        # DIALOG SETTINGS
        dialog.setObjectName("NewProfile")
        dialog.resize(400, 300)

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
        """
        This function is used to set up all the GUI
        It sets up the three labels and text area, define the constraints and set up the buttons
        :return: Nothing
        """
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
        """
        This function is used to define the label of each displayable component according to the locale
        THE CURRENT PROJECT (21/02/2018) DOES NOT SUPPORT MULTILANGUAGE
        :return: Nothing
        """
        _translate = QtCore.QCoreApplication.translate
        new_profile.setWindowTitle(_translate("NewProfile", "Créer un nouveau profil"))
        self.label_last_name.setText(_translate("NewProfile", "Nom"))
        self.label_first_name.setText(_translate("NewProfile", "Prénom"))
        self.label_age.setText(_translate("NewProfile", "Age"))

    def get_first_name(self):
        """
        This function retrieve the content of the text_first_name textEdit
        :return: String containing the first name writen in the text_first_name textEdit
        """
        return self.text_first_name.text()

    def get_last_name(self):
        """
        This function retrieve the content of the text_last_name textEdit
        :return: String containing the last name writen in the text_last_name textEdit
        """
        return self.text_last_name.text()

    def get_age(self):
        """
        This function retrieve the content of the text_age textEdit
        :return: String containing the age writen in the text_age textEdit
        """
        return self.text_age.text()

    @staticmethod
    def get_info():
        """
        This function is used to create a dialog, fill it with the current UI, execute it and get the result.
        :return: String, String, String, Boolean - Each value (first_name, last_name and age) retrieved from the
        text edit and aslo a boolean that indicates if the user confirmed or reject his action
        """
        dialog      = QtWidgets.QDialog()
        ui          = NewProfileDialog(dialog)
        result      = dialog.exec_()
        first_name  = ui.get_first_name()
        last_name   = ui.get_last_name()
        age         = ui.get_age()
        return first_name, last_name, age, result == QDialog.Accepted


