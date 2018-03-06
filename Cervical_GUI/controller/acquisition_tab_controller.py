import os

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QMessageBox

from controller.threads import StartSocketServerThread, StartAcquisitionThread, StopAcquisitionThread, \
    SendContinueThread
from model.file_manager import create_file_with_curves, get_coord
from model.socket_server import SocketServer, PortCount, calculate_time_for_finish
import model.hulls as hl
import model.hull_and_spline as hs
import model.myutils as utl
import model.plot_time as plot_time


DEBUG = True


class AcquisitionTabController(QObject):
    """
        This class is used to handle every action done on the acquisition view
        Here you can find button handler and attributes used to perform acquisition process
    """

    # First values display when the GUI is launched
    INIT_ANGLE                      = 70.0
    INIT_SPEED                      = 25
    INIT_NB_RETURN                  = 5
    INIT_WAIT_TIME                  = 0.2

    # OTHER CONSTANT
    LAST_PROFILE_USED_LIST_LIMIT    = 5
    COUNT_DOWN_TIME                 = "3"
    SPHERE_GREEN_TO_YELLOW_ANGLE    = "0.1"
    SPHERE_YELLOW_TO_RED_ANGLE      = "0.2"
    # TODO FX SI TU VEUX SIMULER UNE ACQUISITION UTILISE tmp1.orpl
    # A LA FIN D'UNE ACQUISITION, LE PROGRAMME LIRA DANS CE FICHIER UNE "FAUSSE" COURBE
    TMP_FILE_PATH                   = "tmp1.orpl"

    # Values used to create the socket and discuss with unity project
    HOST = "localhost"
    PORT = 50007

    def __init__(self, view):
        """
        Function used to create the controller and init each attribute
        :param view: the corresponding view (here acquisition.py)
        """
        super(AcquisitionTabController, self).__init__()

        # ATTRIBUTES
        self.view               = view
        self.selected_movement  = "Lacet"
        self.angle              = AcquisitionTabController.INIT_ANGLE
        self.speed              = AcquisitionTabController.INIT_SPEED
        self.nb_return          = AcquisitionTabController.INIT_NB_RETURN
        self.wait_time          = AcquisitionTabController.INIT_WAIT_TIME
        self.comment            = ""
        self.send_start_thread  = None
        self.send_stop_thread   = None
        self.send               = False
        self.send_continue_thread = None
        self.params             = {}
        self.to_display         = False
        # Attribute curves_on_graph used to list the curves names currently displayed on the graph
        self.curves_on_graph    = []
        # Attribute yaw_pitch_roll used to list the curves values currently displayed on the graph
        self.yaw_pitch_roll     = []

        # THREADS AND SOCKET SERVER
        self.socket_server = SocketServer()

        self.port_counter = PortCount(50007)
        self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
        self.start_server_thread.completeSignal.connect(self.handle_start_server_thread_completion)
        self.start_server_thread.start()

        self.number_of_finish_handlers_to_ignore = 0
        self.send_continue_thread_id = 0

    @pyqtSlot(name="start_stop_button_handler")
    def start_stop_button_handler(self):
        """
        Handler called when the button Start/Stop from acquisition.py (startStopButton) is clicked
        If it has to start:
            - It retrieve the acquisition parameters from the text edits
            - It creates the socket to communicate with Unity exe
            - It sends startAcquisition with parameters retrieved
        If it has to stop:
            - It creates the socket to communicate with Unity exe
            - It sends stopAcquisition to interrupt the Unity exe acquisition process
        :return: Nothing
        """
        if self.view.startStopButton.text() == "Lancer acquisition":
            DEBUG and print('START')
            self.selected_movement = self.view.comboBox.currentText()
            self.angle = self.view.text_angle.value()
            self.speed = self.view.text_speed.value()
            self.nb_return = self.view.text_nb_return.value()
            self.wait_time = self.view.text_wait_time.value()

            # Clear graph to display the next acquisition
            self.view.clear_graph()

            self.params = {"sphereSpeed": str(self.speed), "sphereLimitAngle": str(self.angle),
                           "sphereWaitTime": str(self.wait_time),
                           "sphereCountdownTime": self.COUNT_DOWN_TIME, "sphereRoundTripNumber": str(self.nb_return),
                           "profileName": "guillaumelethug",
                           "sphereGreenToYellowAngle": self.SPHERE_GREEN_TO_YELLOW_ANGLE,
                           "sphereYellowToRedAngle": self.SPHERE_YELLOW_TO_RED_ANGLE}

            DEBUG and print("=== acquisition.py === AcquisitionTab info : \n" +
                  "MOV: " + str(self.view.comboBox.currentText()) + "\n" +
                  "ANGLE: " + str(self.angle) + "\n" +
                  "SPEED: " + str(self.speed) + "\n" +
                  "NB RETURN: " + str(self.nb_return) + "\n" +
                  "TIME LIMIT: " + str(self.wait_time) + "\n")

            self.send_start_thread = StartAcquisitionThread(self.socket_server, self.params)
            self.send_start_thread.completeSignal.connect(self.handle_send_start_thread_completion)
            self.send_start_thread.start()

        elif self.view.startStopButton.text() == "Arrêter acquisition":
            DEBUG and print('STOP')
            self.send_stop_thread = StopAcquisitionThread(self.socket_server)
            self.send_stop_thread.completeSignal.connect(self.handle_send_stop_thread_completion)
            self.send_stop_thread.start()

    @pyqtSlot(str, name="send_finish_thread_completion_handler")
    def handle_send_finish_thread_completion(self, e):
        """
        Handler called when the python GUI needs to tell the Unity GUI that the acquisition can be finished, i.e. when
        the SendFinishThread waited for enough time (until the last stop of the sphere before the end of the
        acquisition.
        It checks taht the send finish thread is the correct one and then set the Start/Stop button to "Finishing
        AcquisitionTab", sends "finishAcquisition" to the Unity GUI, closes the socket server and starts another one.
        :param e: The number of the SendFinishThread that stopped
        :return: Nothing
        """
        DEBUG and print("handle_send_finish_thread_completion")
        if self.number_of_finish_handlers_to_ignore == int(e):
            if self.send:
                # UPDATE BUTTON START/STOP
                self.view.startStopButton.setText("Fin AcquisitionTab...")
                self.view.startStopButton.setStyleSheet("background-color: blue; color:white")
                self.view.startStopButton.setEnabled(False)
                self.socket_server.send("finishAcquisition")
                self.socket_server.close()

                self.socket_server = SocketServer()
                self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
                self.start_server_thread.completeSignal.connect(
                    self.handle_start_server_thread_acquisition_finished_completion)
                self.start_server_thread.start()
                self.number_of_finish_handlers_to_ignore += 1

    @pyqtSlot(str, name="start_server_thread_acquisition_finished_completion_handler")
    def handle_start_server_thread_acquisition_finished_completion(self, e):
        """
        Handler called when the socket server has been initialized and the Unity client connected after an acquisition
        finished.
        It receives the "endAcquisition" signals with the mean and the standard deviation between the eyes and the
        sphere during the acquisition.
        If those values show that the acquisition is not good, it displays a popup asking if the user wants to keep it
        nonetheless.
        It then sets the button to "Start AcquisitionTab"
        :return: Nothing
        """
        DEBUG and print("handle_start_server_thread_acquisition_finished_completion")
        end_acquisition_message = self.socket_server.receive()
        [_, mean, standard_deviation] = end_acquisition_message.decode('utf-8').split(',')
        mean = float(mean.split(':')[1])
        standard_deviation = float(standard_deviation.split(':')[1])

        if not self.is_acquition_correct(mean, standard_deviation):
            confirmation_msg = "L'acquisition ne semble pas correcte. Souhaitez-vous la conserver ?\nMoyenne: {0}" \
                               "\nEcart-type: {1}".format(mean, standard_deviation)
            reply = QMessageBox.question(self.view, 'Mauvaise acquisition',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                DEBUG and print("=== acquisition_tab_controller.py === CONSERVER ACQUISITION")
                # Update graph with tMP file content
                self.view.draw_curves([self.TMP_FILE_PATH], os.getcwd())
                self.view.saveButton.setEnabled(True)
                # TODO FX ICI CODE EXECUTE DES QU'UNE ACQUISITION EST DE MOYENNE QUALITE MAIS L'USER
                # VEUT LA CONSERVER ET EST TERMINEE
                # ICI DESSINER LES MODELES ET LEURS COMPARAISONS
                if self.view.main_window_controller.one_model_loaded():
                    self.display_models(get_coord(self.TMP_FILE_PATH))
                if not self.view.main_window_controller.all_models_loaded():
                    self.to_display = True
            else:
                DEBUG and print("=== acquisition_tab_controller.py === SUPPRIMER ACQUISITION")
                self.view.clear_graph()

                # Empty attribute
                self.curves_on_graph = []

                # Disable save button
                self.view.saveButton.setEnabled(False)

        else:
            self.view.draw_curves([self.TMP_FILE_PATH], os.getcwd())
            self.view.saveButton.setEnabled(True)
            # TODO FX ICI CODE EXECUTE DES QU'UNE ACQUISITION C'EST BIEN PASSE ET EST TERMINEE
            # ICI DESSINER LES MODELES ET LEURS COMPARAISONS
            if self.view.main_window_controller.one_model_loaded():
                self.display_models(get_coord(self.TMP_FILE_PATH))
            if not self.view.main_window_controller.all_models_loaded():
                self.to_display = True

        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Lancer acquisition")
        self.view.startStopButton.setStyleSheet("background-color: green; color:white")
        self.view.startStopButton.setEnabled(True)

        # TODO ADD CONTENT

    def display_models(self, new_coords):
        new_coords = utl.preprocess_data([new_coords])[0]
        path_hs = self.view.main_window_controller.path_model_hull_and_spline
        path_hull = self.view.main_window_controller.path_model_hulls
        path_wavelet = self.view.main_window_controller.path_model_wavelet

        if path_hs != "":
            mdl_hull_spline = hs.load_model(path_hs)
            res_comparison, to_plot_pitch, to_plot_roll = hs.compare_to_model(new_coords, mdl_hull_spline)
            hull_pitch, hull_roll, spline_std_pitch, spline_std_roll = mdl_hull_spline
            # Display figures
            self.view.parent.tab_hull_and_splines.canvas_left_modeling.plot_hull_spline(hull_pitch, (
                to_plot_pitch['xs'], to_plot_pitch['ys']), to_plot_pitch['curve'], 'pitch')
            self.view.parent.tab_hull_and_splines.canvas_right_modeling.plot_hull_spline(hull_roll, (
                to_plot_roll['xs'], to_plot_roll['ys']), to_plot_roll['curve'], 'roll')
            # Display results
            self.view.parent.tab_hull_and_splines.label_left_variability_score.setText(
                str(res_comparison['err_spline_pitch'])[:7])
            self.view.parent.tab_hull_and_splines.label_right_variability_score.setText(
                str(res_comparison['err_spline_roll'])[:7])
            self.view.parent.tab_hull_and_splines.label_left_rate_value.setText(
                "{:.2%}".format(res_comparison['rate_out_pitch']))
            self.view.parent.tab_hull_and_splines.label_right_rate_value.setText(
                "{:.2%}".format(res_comparison['rate_out_roll']))

        if path_hull != "":
            mdl_hull = hl.load_model(self.view.main_window_controller.path_model_hulls)
            ocsvm_mdl = mdl_hull[0]
            size_grid = mdl_hull[3]
            alpha = mdl_hull[4]
            healthy, grid_pitch, hull_pitch, grid_roll, hull_roll = hl.compare_to_model(new_coords, ocsvm_mdl,
                                                                                        size_grid=size_grid,
                                                                                        alpha=alpha)
            self.view.parent.tab_hulls.canvas_left_modeling.plot_discrete_hull(grid_pitch[0], grid_pitch[1],
                                                                                   hull_pitch)
            self.view.parent.tab_hulls.canvas_right_modeling.plot_discrete_hull(grid_roll[0], grid_roll[1],
                                                                                    hull_roll)
            # TODO ALSO PRINT HEALTHY

        if path_wavelet != "":
            yaw, pitch, roll, _ = plot_time.load_model(self.view.main_window_controller.path_model_wavelet)
            mean_coords = yaw, pitch, roll
            self.view.parent.tab_wavelet.canvas_up_left_modeling.plot_final_time(new_coords, mean_coords, 1)
            self.view.parent.tab_wavelet.canvas_down_left_modeling.plot_final_time(new_coords, mean_coords, 2)
            self.view.parent.tab_wavelet.canvas_up_right_modeling.plot_final_time(new_coords, mean_coords, 3)
            self.view.parent.tab_wavelet.canvas_down_right_modeling.plot_final_time(new_coords, mean_coords, 4)



    @pyqtSlot(str, name="start_server_thread_completion_handler")
    def handle_start_server_thread_completion(self, e):
        """
        Handler called when the socket server is first started and the launch of the GUI.
         If the Unity client is connected and a profile is loaded, it enables the Start/Stop button
        :return: Nothing
        """
        DEBUG and print("handle_start_server_thread_completion")
        self.view.connected = True
        if self.view.profile_loaded:
            self.view.startStopButton.setEnabled(True)
            self.view.startStopButton.setStyleSheet("background-color: green; color:white")

    @pyqtSlot(str, name="start_server_thread_acquisition_started_completion_handler")
    def handle_start_server_thread_acquisition_started_completion(self, e):
        """
        Handler called when "startAcquisition" was sent and a new socket server was started and Unity connected to it
        It receives the "startAcquisitionAck" and then sets the button to "Stop AcquisitionTab"
        It starts a "sendContinueThread" that will wait until the last stop of the sphere.
        It allows to send a "stopAcquisition" until the thread finishes. After that, the acquisition finishes
        normally
        :return: Nothing
        """
        DEBUG and print("handle_start_server_thread_acquisition_started_completion")
        self.socket_server.receive()
        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Arrêter acquisition")
        self.view.startStopButton.setStyleSheet("background-color: red; color:white")
        self.view.startStopButton.setEnabled(True)
        time_to_wait = calculate_time_for_finish(self.params)
        self.send = True
        self.send_continue_thread = SendContinueThread(self.socket_server, self.start_server_thread, time_to_wait,
                                                       self.port_counter, self.send_continue_thread_id)
        
        self.send_continue_thread_id += 1
        self.send_continue_thread.completeSignal.connect(self.handle_send_finish_thread_completion)
        self.send_continue_thread.start()
        #self.port_counter.reset()

    @pyqtSlot(str, name="handle_start_server_thread_acquisition_stopped_completion")
    def handle_start_server_thread_acquisition_stopped_completion(self, e):
        """
        Handler called when "stopAcquisition" was sent and a new socket server was started and Unity connected to it
        It receives "stopAcquisitionAck" and sets the button to "Start AcquisitionTab"
        :return: Nothing
        """
        DEBUG and print("handle_start_server_thread_acquisition_stopped_completion")
        self.socket_server.receive()
        self.view.startStopButton.setText("Lancer acquisition")
        self.view.startStopButton.setStyleSheet("background-color: green; color:white")
        self.view.startStopButton.setEnabled(True)
        self.view.saveButton.setEnabled(False)

    @pyqtSlot(str, name="handle_send_start_thread_completion")
    def handle_send_start_thread_completion(self, e):
        """
        Handler called when "startAcquisition" was just sent.
        It starts a new thread in charge of starting a new socket server.
        It then changes the button to "Starting AcquisitionTab..."
        :return: Nothing
        """
        DEBUG and print("handle_send_start_thread_completion")
        # UPDATE BUTTON START/STOP OIZHUIAHDIUZAHOIDZL
        self.view.startStopButton.setText("Lancement AcquisitionTab...")
        self.view.startStopButton.setStyleSheet("background-color: blue; color:white")
        self.view.startStopButton.setEnabled(False)
        self.view.saveButton.setEnabled(False)
        self.socket_server.close()
        self.socket_server = SocketServer()
        self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
        self.start_server_thread.completeSignal.connect(self.handle_start_server_thread_acquisition_started_completion)
        self.start_server_thread.start()

    @pyqtSlot(str, name="send_stop_thread_completion_handler")
    def handle_send_stop_thread_completion(self, e):
        """
        Handler called when "stopAcquisition" was just sent.
        It starts a new thread in charge of starting a new socket server.
        It then changes the button to "Stopping AcquisitionTab..." and tells the FinishAcquisitionCompletion handler
        to ignore this specific FinishAcquisition thread
        :return: Nothing
        """
        DEBUG and print("handle_send_stop_thread_completion")
        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Arrêt AcquisitionTab...")
        self.view.startStopButton.setStyleSheet("background-color: blue; color:white")
        self.view.startStopButton.setEnabled(False)
        self.socket_server.close()
        self.send = False
        self.number_of_finish_handlers_to_ignore = self.number_of_finish_handlers_to_ignore + 1
        self.socket_server = SocketServer()
        self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
        self.start_server_thread.completeSignal.connect(self.handle_start_server_thread_acquisition_stopped_completion)
        self.start_server_thread.start()

    @pyqtSlot(name="empty_graph_button_handler")
    def empty_graph_button_handler(self):
        """
        Handler called when the empty button from acquisition.py (emptyGraph) is clicked
        It checks if there is some curves currently display on graph and:
            - If there is some:
                - It displays a confirmation dialog to inform the user is going to remove X curves (X = nb of curves)
                - If the user confirms, it remove them
                - Otherwise it cancel the operation
            - If there is not any:
                - It displays a dialog that inform the user that there is not any curves currently displayed
        :return: Nothing
        """
        if len(self.curves_on_graph) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Graphiques vide")
            msg.setInformativeText("Aucune courbes n'est affiché actuellement")
            msg.setWindowTitle("Information")
            msg.exec()
        else:
            confirmation_msg = "Etes-vous sûr de vouloir supprimer des graphiques toutes " \
                               "les courbes affichées ? (" + str(len(self.curves_on_graph)) + \
                               (" courbes)" if len(self.curves_on_graph) > 1 else " courbe)")
            reply = QMessageBox.question(self.view, 'Attention !',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                DEBUG and print("=== acquisition_tab_controller.py === SUPPRESION EN COURS")
                self.view.clear_graph()

                # Empty attribute
                self.curves_on_graph    = []

                # Disable save button
                self.view.saveButton.setEnabled(True)

            else:
                DEBUG and print("=== acquisition_tab_controller.py === ANNULATION")

    @pyqtSlot(name="save_curves_button_handler")
    def save_curves_button_handler(self):
        """
        Handler called when the save curves button from acquisition.py (saveButton) is clicked
        It basically retrieves the acquisition parameters, comments and the data given by Unity exe
        and save them into a file
        :return: Nothing
        """
        DEBUG and print('=== acquisition_tab_controller.py === SAVE CURVES')

        # RETRIEVE THE FIRST ELEMENT BECAUSE IT MUST HAVE ONLY ONE CURVE ON THE GRAPH
        data = self.yaw_pitch_roll[0]

        self.selected_movement  = self.view.comboBox.currentText()
        self.angle              = self.view.text_angle.text()
        self.speed              = self.view.text_speed.text()
        self.nb_return          = self.view.text_nb_return.text()
        self.wait_time          = self.view.text_wait_time.text()
        self.comment            = self.view.text_area_comment.toPlainText()

        param = [self.selected_movement, self.angle, self.speed, self.nb_return, self.wait_time, self.comment]

        # Write Data into file with parameters and comment
        directory = self.view.main_window_controller.last_name.strip("\n") + "_" + \
                    self.view.main_window_controller.first_name.strip("\n") + "_" + \
                    self.view.main_window_controller.age.strip("\n") + "/"
        print("%%%%% DIRECTORY " + directory)
        success = create_file_with_curves(directory, data, param)

        if success:
            self.view.saveButton.setEnabled(False)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Une erreur est survenue")
            msg.setInformativeText("La sauvegarde de la courbe n'a pas pu être effectuée, veuillez réessayer")
            msg.setWindowTitle("Erreur")
            msg.exec()
            pass

    def is_acquition_correct(self, mean, standard_deviation):
        """
        Determines whether an acquisition was correct from its mean and standard deviation
        :param mean: The mean of the acquisition
        :param standard_deviation: The standard deviation of the acquisition
        :return: A boolean, true if and only if the aquisition is correct
        """
        return mean > 1.7 and standard_deviation < 0.5