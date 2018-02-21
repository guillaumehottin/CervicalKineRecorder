import os
import webbrowser

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from model.file_manager import create_directory, get_file_name_from_absolute_path, \
    add_profile_used
from view.curves_dialog import CurvesDialog
from view.model_generator_dialog import ModelGeneratorDialog
from view.new_profile_dialog import NewProfileDialog

PATH_TO_STORE_FILE      = "./data/"


class MyWindowController(QObject):

    def __init__(self, view):
        super(MyWindowController, self).__init__()

        # ATTRIBUTES
        self.view               = view
        self.directory_path     = ""
        self.first_name         = "Prénom"
        self.last_name          = "Nom"
        self.age                = "âge"

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
                self.view.update_ui(True, self.first_name, self.last_name, self.age)

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
                                                        PATH_TO_STORE_FILE, QFileDialog.ShowDirsOnly))

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

            self.view.update_ui(True, self.first_name, self.last_name, self.age)

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
        sending_button  = self.view.sender()
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
                self.view.update_ui(True, self.first_name, self.last_name, self.age)

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
        print('LOAD CURVES: ' + self.directory_path)
        curves_on_graph, accepted = CurvesDialog.get_result(self.directory_path,
                                                                 self.view.tab_acquisition.get_curves_on_graph())
        print("CURVES SELECTED ",  str(curves_on_graph))
        # The user choose some curves
        if accepted:
            # Empty attributes and graph
            self.view.tab_acquisition.draw_curves(curves_on_graph, self.directory_path)

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="load_files_model_handler")
    def load_files_model_handler(self):
        print('LOAD FILES' + self.directory_path)
        directories_for_model, accepted = ModelGeneratorDialog.get_result(self.directory_path)

        # The user choose some directories
        if accepted:
            print("=== acquisition.py === selected directories: " + str(directories_for_model))

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="about_menu_handler")
    def about_menu_handler(self):
        print('ABOUT')
        webbrowser.open(GIT_LINK, new=2)