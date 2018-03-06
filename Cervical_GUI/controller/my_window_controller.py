import os
import webbrowser

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from model import hull_and_spline, hulls, plot_time
from model.file_manager import create_directory, get_file_name_from_absolute_path, \
    add_profile_used, get_coord
from view.curves_dialog import CurvesDialog
from view.model_generator_dialog import ModelGeneratorDialog
from view.new_profile_dialog import NewProfileDialog

DEBUG               = False


class MyWindowController(QObject):
    """
    This class is used to define all the logic behing my_window.py GUI
    Here you will find all button handler
    """

    PATH_TO_STORE_FILE              = "./data/"
    PATH_TO_STORE_MODELS            = "./models/"
    EXTENSION_HULLS_MODEL           = ".mdlhl"
    EXTENSION_HULLS_SPLINES_MODEL   = ".mdlhs"
    EXTENSION_WAVELET_MODEL         = ".mdlwvl"
    GIT_LINK = "https://github.com/guillaumehottin/projetlong"

    def __init__(self, view):
        """
        Function used to create the controller and init each attribute
        :param view: the corresponding view (here acquisition.py)
        """
        super(MyWindowController, self).__init__()

        # ATTRIBUTES
        self.view               = view
        self.directory_path     = ""
        self.first_name         = "Prénom"
        self.last_name          = "Nom"
        self.age                = "âge"
        
        # MODELS
        self.path_model_hulls           = ""
        self.path_model_hull_and_spline = ""
        self.path_model_wavelet        = ""

    @pyqtSlot(name="new_profile_menu_handler")
    def new_profile_menu_handler(self):
        """
        Handler called when the new profile menu is triggered
        It open a new_profile_dialog.py to allow the user to fill in first name, last name and age
        If a same profile (same firstname, lastname, age) is already existing it displays a pop-up
        If everything is OK, It automagically update the UI according to the selected profile
        :return: Nothing
        """
        self.first_name, self.last_name, self.age, accepted = NewProfileDialog.get_info()

        if accepted:
            DEBUG and print("=== my_window_controller.py === User info : \n " +
                    "FIRST NAME " + self.first_name + "\n" +
                    "LAST NAME " + self.last_name + "\n" +
                    "AGE " + self.age)
            try:
                self.directory_path = create_directory(self.last_name.lower() + "_" + self.first_name.lower() +
                                                       "_" + self.age)
                # Update label value
                self.view.update_ui(True, self.first_name, self.last_name, self.age)

                DEBUG and print("=== my_window_controller.py === DIRECTORY CREATED AT: " + self.directory_path)

            except OSError:
                DEBUG and print("=== my_window_controller.py === DIRECTORY ALREADY EXIST AT: " + self.directory_path)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Dossier déjà existant")
                msg.setInformativeText("Le patient que vous avez voulu créé existe déjà, veuillez changer de nom")
                msg.setWindowTitle("Erreur")
                msg.exec()

        else:
            DEBUG and print("=== my_window_controller.py === OPERATION CANCELED")

    @pyqtSlot(name="load_profile_menu_handler")
    def load_profile_menu_handler(self):
        """
        Handler called when the load profile menu is triggered
        It opens a browse directory dialog and allow the user to select a directory
        If the directory selected is already opened in the GUI, it displays a pop up and does not open it again
        If everything is ok, It automagically update the UI according to the selected profile
        :return: Nothing
        """
        new_path = str(QFileDialog.getExistingDirectory(self.view, "Sélectionner un dossier",
                                                        self.PATH_TO_STORE_FILE, QFileDialog.ShowDirsOnly))

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

        DEBUG and print("=== acquisition.py === FOLDER LOADED : " + self.directory_path)

        directory_name = get_file_name_from_absolute_path(self.directory_path)

        try:
            [self.last_name, self.first_name, self.age] = directory_name.split("_")

            # Add profile to "last_profile_used" file
            add_profile_used(directory_name)

            self.view.update_ui(True, self.first_name, self.last_name, self.age)

            DEBUG and print("=== acquisition.py === User info : \n " +
                  "FIRST NAME " + self.first_name + "\n" +
                  "LAST NAME " + self.last_name + "\n" +
                  "AGE " + self.age)

        except ValueError:
            # DISPLAY POP UP ERROR AND DO NOTHING
            DEBUG and print("=== acquisition.py === INCORRECT FOLDER NAME")
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
        """
        Handler called when a profile is loaded from the last profile used list
        It automagically update the UI according to the selected profile
        :return: Nothing
        """
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
                self.directory_path = os.path.abspath(self.PATH_TO_STORE_FILE + text_button.replace(" ", "_")).strip("\n")
                self.view.update_ui(True, self.first_name, self.last_name, self.age)

        except ValueError:
            # DISPLAY POP UP ERROR AND DO NOTHING
            DEBUG and print("=== acquisition.py === INCORRECT FOLDER NAME")
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
        """
        Handler called when the load curves menu is triggered
        It opens the curves_dialog.py and allow the user to select the curves he wants to display on the graph
        If the user confirm his operation, it updates the graph according to the selected curves
        Otherwise it does nothing
        :return: Nothing
        """
        DEBUG and print('=== my_window_controller.py === LOAD CURVES: ' + self.directory_path)
        curves_on_graph, accepted = CurvesDialog.get_result(self.directory_path,
                                                                 self.view.tab_acquisition.get_curves_on_graph())
        DEBUG and print("=== my_window_controller.py === CURVES SELECTED ",  str(curves_on_graph))
        # The user choose some curves
        if accepted:
            # Empty attributes and graph
            self.view.tab_acquisition.draw_curves(curves_on_graph, self.directory_path)

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="load_files_model_handler")
    def create_model_handler(self):
        """
        Handler called when the regenerate model menu is triggered
        It opens the model_generator_dialog and allow the user to select the profile he wants to use to
        generate the the model
        According to them it regenerates the model
        :return: Nothing
        """
        DEBUG and print('LOAD FILES' + self.directory_path)
        directories_for_model, model_name, accepted = ModelGeneratorDialog.get_result(self.directory_path)

        # The user choose some directories
        if accepted:
            DEBUG and print("=== acquisition.py === selected directories: " + str(directories_for_model))
            DEBUG and print("=== acquisition.py === model name: " + str(model_name))

            if len(directories_for_model) == 0:
                DEBUG and print("=== acquisition.py === None patient selected, clearing the graph")
                self.view.tab_hull_and_splines.clear_graph()
                self.view.tab_hulls.clear_graph()
                self.view.tab_wavelet.clear_graph()
            else:
                # TODO regenerates model with given patient and file name
                directories_for_model = ['./data/' + d for d in directories_for_model]
                hulls.save_model(directories_for_model, './models/' + model_name + '_hull' + self.EXTENSION_HULLS_MODEL)
                hull_and_spline.save_model(directories_for_model, './models/' + model_name + '_hull_and_spline' +
                                           self.EXTENSION_HULLS_SPLINES_MODEL)
                plot_time.save_model(directories_for_model, './models/' + model_name + '_time_series' + self.EXTENSION_WAVELET_MODEL)

        else:  # The user cancel his operation
            pass

    @pyqtSlot(name="load_model_menu_handler")
    def load_model_handler(self):
        """
        Handler called when the load model menu is triggered
        It opens a browse directory dialog and allow the user to select a file
        If the file selected does not match the pattern we want we display an error
        :return: Nothing
        """
        my_filter = "Model file (*" + self.EXTENSION_HULLS_SPLINES_MODEL + " *" + self.EXTENSION_HULLS_MODEL + " *" +\
                 self.EXTENSION_WAVELET_MODEL + ") ;; All files (*)"

        model_path, _ = QFileDialog.getOpenFileNames(self.view, caption="Sélectionner un modèle",
                                                  filter=my_filter, directory=self.PATH_TO_STORE_MODELS)
        # If the user canceled
        if not model_path:
            return

        nb_hulls_model = sum(1 for curr_path in model_path \
                             if os.path.splitext(curr_path)[1] == self.EXTENSION_HULLS_MODEL)
        print("NBBBBB HULLS " + str(nb_hulls_model))

        nb_hull_and_splines_model = sum(1 for curr_path in model_path \
                             if os.path.splitext(curr_path)[1] == self.EXTENSION_HULLS_SPLINES_MODEL)
        print("NBBBBB HULLS AND SPLINES " + str(nb_hull_and_splines_model))

        nb_wavelet_model = sum(1 for curr_path in model_path \
                             if os.path.splitext(curr_path)[1] == self.EXTENSION_WAVELET_MODEL)
        print("NBBBBB WAVELET " + str(nb_wavelet_model))

        informative_text = "Vous avez sélectionné deux modèles du type TYPE. \n" +\
                           "Veuillez faire attention à ne sélectionner qu'un seul modèle du type TYPE " +\
                           "(vérifiable grâce au nom du fichier ainsi qu'à son extension 'EXTENSION')"

        if nb_hulls_model > 1:
            informative_text = informative_text.replace("TYPE", "Hulls")
            informative_text = informative_text.replace("EXTENSION", self.EXTENSION_HULLS_MODEL)

        if nb_hull_and_splines_model > 1:
            informative_text = informative_text.replace("TYPE", "Hulls and Splines")
            informative_text = informative_text.replace("EXTENSION", self.EXTENSION_HULLS_SPLINES_MODEL)

        if nb_wavelet_model > 1:
            informative_text = informative_text.replace("TYPE", "Wavelet")
            informative_text = informative_text.replace("EXTENSION", self.EXTENSION_WAVELET_MODEL)

        if nb_wavelet_model > 1 or nb_hull_and_splines_model > 1 or nb_hulls_model > 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Modèles en conflits")
            msg.setInformativeText(informative_text)
            msg.setWindowTitle("Attention")
            msg.exec()
            return

        # Go through each selected path
        for path in model_path:

            try:
                _, file_extension = os.path.splitext(path)

                acquisition_tab_controller = self.view.tab_acquisition.acquisition_controller
                if file_extension == self.EXTENSION_HULLS_MODEL:
                    self.path_model_hulls = path
                    if acquisition_tab_controller.to_display:
                        acquisition_tab_controller.display_models(get_coord(acquisition_tab_controller.TMP_FILE_PATH))

                elif file_extension == self.EXTENSION_HULLS_SPLINES_MODEL:
                    self.path_model_hull_and_spline = path
                    if acquisition_tab_controller.to_display:
                        acquisition_tab_controller.display_models(get_coord(acquisition_tab_controller.TMP_FILE_PATH))

                elif file_extension == self.EXTENSION_WAVELET_MODEL:
                    self.path_model_wavelet = path
                    if acquisition_tab_controller.to_display:
                        acquisition_tab_controller.display_models(get_coord(acquisition_tab_controller.TMP_FILE_PATH))

                if self.all_models_loaded():
                    acquisition_tab_controller.to_display = False

            except ValueError:
                # DISPLAY POP UP ERROR AND DO NOTHING
                DEBUG and print("=== acquisition.py === INCORRECT FILE NAME")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Format de fichier incorrect")
                msg.setInformativeText("Le fichier que vous avez sélectionné ne correspond pas à un fichier modèle")
                msg.setWindowTitle("Erreur")
                msg.exec()
                return

        if len(model_path) > 1:
            text = "Les " + str(len(model_path)) + " modèles ont été chargés avec succès"
        else:
            text = "Le modèle a été chargé avec succès"

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Modèles chargés avec succès")
        msg.exec()
        return

    def one_model_loaded(self):
        return self.path_model_hull_and_spline != "" or self.path_model_hulls != "" or self.path_model_wavelet != ""

    def all_models_loaded(self):
        return self.path_model_hull_and_spline != "" and self.path_model_hulls != "" and self.path_model_wavelet != ""

    @pyqtSlot(name="about_menu_handler")
    def about_menu_handler(self):
        """
        Handler called when the about menu is called
        It opens a web browser to the link of our github project
        :return:
        """
        DEBUG and print('=== my_window_controller.py === ABOUT')
        webbrowser.open(self.GIT_LINK, new=2)