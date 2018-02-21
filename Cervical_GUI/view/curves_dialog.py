# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog

from model.file_manager import get_all_directory_files

DEBUG               = True


class CurvesDialog(object):
    """
    This class is used to define the load curve dialog
    Here you can find list view set up, curves file retrieval
    """

    def __init__(self, curves_dialog, directory_path, already_selected_curves):
        """
        This function is used to declare and initialize all class attributes
        :param curves_dialog: The dialog in which this GUI will be displayed
        :param directory_path: String containing the path in which we have to look for curves files
        :param already_selected_curves: String list containing the curves already displayed on the graph
        """
        curves_dialog.setObjectName("CurvesDialog")
        curves_dialog.resize(550, 450)

        # ATTRIBUTES
        self.directory_path             = directory_path
        self.already_selected_curves    = already_selected_curves
        self.parent                     = curves_dialog

        # VBOX LAYOUT
        self.vertical_layout = QtWidgets.QVBoxLayout(curves_dialog)

        # BUTTON BOX
        self.buttonBox = QtWidgets.QDialogButtonBox(curves_dialog)

        # SCROLL AREA
        self.scrollArea = QtWidgets.QScrollArea(self.vertical_layout.widget())

        # LIST VIEW
        self.listView = QtWidgets.QListView(self.scrollArea)

        # MODEL
        self.model = QStandardItemModel(self.listView)

        # END SETUP UI
        self.setup_ui()

    def setup_ui(self):
        """
        This function is used to set up all the GUI
        It sets up the scroll area, retrieves the list of curves name and fills in the list view
        :return: Nothing
        """
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
        list_curves = get_all_directory_files(self.directory_path)

        if len(list_curves) > 0:
            DEBUG and print("=== curves_dialog.py === LIST CURVES: " + str(list_curves))
            DEBUG and print("=== curves_dialog.py === ALREADY SELECTED CURVES: " + str(self.already_selected_curves))
            for i in range(0, len(list_curves)):
                # Add curve name as first column
                item_curve_name = QStandardItem(list_curves[i])
                item_curve_name.setCheckable(True)
                if list_curves[i] in self.already_selected_curves:
                    # Set checkbox checked
                    item_curve_name.setCheckState(2)

                 # TODO ADD PARAMETERS
                # Join DIRCETORY_PATH/data/FILENAME
                # path_joined = os.path.join(self.directory_path, list_curves[i])
                # [_, angle, speed, _, _, _] = get_param_from_file(path_joined)
                #
                # # Add parameters as 2nd and 3rd row
                # item_param_angle = QStandardItem(str(angle) + "°")
                # item_param_speed = QStandardItem(str(speed) + "°/s")
                # self.model.setItem(i, 2, item_param_angle)
                # self.model.setItem(i, 3, item_param_speed)
                self.model.appendRow(item_curve_name)

        else:
            item_curve_name = QStandardItem("Aucune courbe n'est disponible pour ce profil")
            item_curve_name.setCheckable(False)
            self.model.appendRow(item_curve_name)

        self.listView.setModel(self.model)

        # BUTTON BOX
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.parent.accept)
        self.buttonBox.rejected.connect(self.parent.reject)
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
        self.parent.setWindowTitle(_translate("Dialog", "Charger des courbes"))

    def get_selected_curves(self):
        """
        This functin is used to go through all the model and retrieve the selected curves
        :return: String list containing the selected curves
        """
        DEBUG and print("=== curves_dialog.py === Get selected curves")
        selected_curves = []
        i = 0
        while self.model.item(i):
            if self.model.item(i).checkState():
                selected_curves.append(self.model.item(i).text())
            i += 1

        return selected_curves

    # static method to create the dialog and return (first_name, last_name, age, accepted)
    @staticmethod
    def get_result(directory_path, already_selected_curves):
        """
        This function is used to create a dialog, fill it with the current UI, execute it and get the result.
        :param directory_path: String, the path in which we have to look for the curves files
        :param already_selected_curves: String list, the list of curves already displayed in the graph anc which will
                already checked when displayed
        :return: String list, Boolean - The list of selected curves names and a boolean which indicates if
        the user has confirm or reject his action
        """
        dialog          = QtWidgets.QDialog()
        ui              = CurvesDialog(dialog, directory_path, already_selected_curves)
        result          = dialog.exec_()
        selected_curves = ui.get_selected_curves()

        return selected_curves, result == QDialog.Accepted
