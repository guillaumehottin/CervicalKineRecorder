from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QMessageBox

from controller.threads import StartSocketServerThread, StartAcquisitionThread, StopAcquisitionThread, \
    SendContinueThread
from model.file_manager import create_file_with_curves
from model.socket_server import SocketServer, PortCount, calculate_time_for_finish

DEBUG = False


class AcquisitionController(QObject):
    """
        This class is used to handle every action done on the acquisition view
        Here you can find button handler and attributes used to perform acquisition process
    """

    # First values display when the GUI is launched
    INIT_ANGLE = 70.0
    INIT_SPEED = 25
    INIT_NB_RETURN = 5
    INIT_WAIT_TIME = 0.2
    LAST_PROFILE_USED_LIST_LIMIT = 5

    # Values used to create the socket and discuss with unity project
    HOST = "localhost"
    PORT = 50007

    def __init__(self, view):
        """
        Function used to create the controller and init each attribute
        :param view: the corresponding view (here acquisition.py)
        """
        super(AcquisitionController, self).__init__()

        # ATTRIBUTES
        self.view               = view
        self.selected_movement  = "Lacet"
        self.angle              = AcquisitionController.INIT_ANGLE
        self.speed              = AcquisitionController.INIT_SPEED
        self.nb_return          = AcquisitionController.INIT_NB_RETURN
        self.wait_time          = AcquisitionController.INIT_WAIT_TIME
        self.comment            = ""
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
    #
    # @pyqtSlot(name="start_stop_button_handler")
    # def start_stop_button_handler(self):
    #     """
    #     Handler called when the button Start/Stop from acquisition.py (startStopButton) is clicked
    #     If it has to start:
    #         - It retrieve the acquisition parameters from the text edits
    #         - It creates the socket to communicate with Unity exe
    #         - It sends startAcquisition with parameters retrieved
    #     If it has to stop:
    #         - It creates the socket to communicate with Unity exe
    #         - It sends stopAcquisition to interrupt the Unity exe acquisition process
    #     :return: Nothing
    #     """
    #     if self.view.startStopButton.text() == "Lancer acquisition":
    #         DEBUG and print('=== acquisition_controller.py === START')
    #         self.selected_movement = self.view.comboBox.currentText()
    #         self.angle = self.view.text_angle.text()
    #         self.speed = self.view.text_speed.text()
    #         self.nb_return = self.view.text_nb_return.text()
    #         self.wait_time = self.view.text_wait_time.text()
    #
    #         # CONF = {"sphereSpeed": str(self.speed), "sphereLimitAngle": str(self.angle), "sphereWaitTime": str(self.wait_time),
    #         #         "sphereCountdownTime": "3", "sphereRoundTripNumber": str(self.nb_return),
    #         #         "profileName": "guillaumelethug", "sphereGreenToYellowAngle": "0.1", "sphereYellowToRedAngle": "0.2"}
    #         #
    #         #
    #         # DEBUG and print("=== acquisition.py === Acquisition info : \n" +
    #         #         "MOV: " + str(self.comboBox.currentText()) + "\n" +
    #         #         "ANGLE: " + str(self.angle) + "\n" +
    #         #         "SPEED: " + str(self.speed) + "\n" +
    #         #         "NB RETURN: " + str(self.nb_return) + "\n" +
    #         #         "TIME LIMIT: " + str(self.wait_time) + "\n")
    #         #
    #         #
    #         #
    #         # message = build_startAcquisition_message(CONF)
    #         #
    #         # self.sock_serv.send(message)
    #         # self.sock_serv.close()
    #         #
    #         # self.sock_serv = SocketServer()
    #         # self.sock_serv.start(HOST, PORT)
    #         #
    #         # DEBUG and print(self.sock_serv.receive())
    #         #
    #         # time_to_wait = calculate_time_for_finish(CONF)
    #         # self.send_continue_thread = SendContinue(self.sock_serv, time_to_wait)
    #         # self.send_continue_thread.start()
    #         #
    #         #
    #
    #         # TODO LAUNCH ACQUISITION
    #
    #         # UPDATE BUTTON START/STOP
    #         self.view.startStopButton.setText("Arrêter acquisition")
    #         self.view.startStopButton.setStyleSheet("background-color: red; color:white")
    #
    #     elif self.view.startStopButton.text() == "Arrêter acquisition":
    #         DEBUG and print('=== acquisition_controller.py === STOP')
    #         # TODO STOP ACQUISITION
    #         # self.sock_serv.send("stopAcquisition")
    #         # self.sock_serv.close()
    #         # DEBUG and print("SENT")
    #         # self.sock_serv = SocketServer()
    #         # DEBUG and print("NEW")
    #         # self.sock_serv.start(AcquisitionController.HOST, AcquisitionController.PORT)
    #         # DEBUG and print("started")
    #         # DEBUG and print(self.sock_serv.receive())
    #         # self.sock_serv.close()
    #         self.view.startStopButton.setText("Lancer acquisition")
    #         self.view.startStopButton.setStyleSheet("background-color: green; color:white")
    #         # self.send_continue_thread.send = False
    #         # self.sock_serv = SocketServer()
    #         # self.sock_serv.start(AcquisitionController.HOST, AcquisitionController.PORT)

    @pyqtSlot(name="start_stop_button_handler")
    def start_stop_button_handler(self):

        if self.view.startStopButton.text() == "Lancer acquisition":
            print('START')
            self.selected_movement = self.view.comboBox.currentText()
            self.angle = self.view.text_angle.text()
            self.speed = self.view.text_speed.text()
            self.nb_return = self.view.text_nb_return.text()
            self.wait_time = self.view.text_wait_time.text()

            self.params = {"sphereSpeed": str(self.speed), "sphereLimitAngle": str(self.angle),
                           "sphereWaitTime": str(self.wait_time),
                           "sphereCountdownTime": "3", "sphereRoundTripNumber": str(self.nb_return),
                           "profileName": "guillaumelethug", "sphereGreenToYellowAngle": "0.1",
                           "sphereYellowToRedAngle": "0.2"}

            print("=== acquisition.py === Acquisition info : \n" +
                  "MOV: " + str(self.view.comboBox.currentText()) + "\n" +
                  "ANGLE: " + str(self.angle) + "\n" +
                  "SPEED: " + str(self.speed) + "\n" +
                  "NB RETURN: " + str(self.nb_return) + "\n" +
                  "TIME LIMIT: " + str(self.wait_time) + "\n")

            self.send_start_thread = StartAcquisitionThread(self.socket_server, self.params)
            self.send_start_thread.completeSignal.connect(self.handle_send_start_thread_completion)
            self.send_start_thread.start()


        elif self.view.startStopButton.text() == "Arrêter acquisition":
            print('STOP')
            self.send_stop_thread = StopAcquisitionThread(self.socket_server)
            self.send_stop_thread.completeSignal.connect(self.handle_send_stop_thread_completion)
            self.send_stop_thread.start()

    @pyqtSlot(str, name="send_finish_thread_completion_handler")
    def handle_send_finish_thread_completion(self, e):
        if self.number_of_finish_handlers_to_ignore == 0:
            if self.send:
                self.socket_server.send("finishAcquisition")
                self.socket_server.close()

                self.socket_server = SocketServer()
                self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
                self.start_server_thread.completeSignal.connect(
                    self.handle_start_server_thread_acquisition_finished_completion)
                self.start_server_thread.start()
        else:
            self.number_of_finish_handlers_to_ignore = self.number_of_finish_handlers_to_ignore - 1

    @pyqtSlot(str, name="start_server_thread_acquisition_finished_completion_handler")
    def handle_start_server_thread_acquisition_finished_completion(self, e):
        print(self.socket_server.receive())
        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Lancer acquisition")
        self.view.startStopButton.setStyleSheet("background-color: green; color:white")

    @pyqtSlot(str, name="start_server_thread_completion_handler")
    def handle_start_server_thread_completion(self, e):
        print("server started")

    @pyqtSlot(str, name="start_server_thread_acquisition_started_completion_handler")
    def handle_start_server_thread_acquisition_started_completion(self, e):
        print(self.socket_server.receive())
        time_to_wait = calculate_time_for_finish(self.params)
        self.send = True
        self.send_continue_thread = SendContinueThread(self.socket_server, self.start_server_thread, time_to_wait,
                                                       self.port_counter)
        self.send_continue_thread.completeSignal.connect(self.handle_send_finish_thread_completion)
        self.send_continue_thread.start()

    @pyqtSlot(str, name="start_server_thread_acquisition_stopped_completion_handler")
    def handle_start_server_thread_acquisition_stopped_completion(self, e):
        print(self.socket_server.receive())

    @pyqtSlot(str, name="send_start_thread_completion_handler")
    def handle_send_start_thread_completion(self, e):
        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Arrêter acquisition")
        self.view.startStopButton.setStyleSheet("background-color: red; color:white")
        self.socket_server.close()
        self.socket_server = SocketServer()
        self.start_server_thread = StartSocketServerThread(self.socket_server, self.port_counter)
        self.start_server_thread.completeSignal.connect(self.handle_start_server_thread_acquisition_started_completion)
        self.start_server_thread.start()

    @pyqtSlot(str, name="send_stop_thread_completion_handler")
    def handle_send_stop_thread_completion(self, e):
        # UPDATE BUTTON START/STOP
        self.view.startStopButton.setText("Lancer acquisition")
        self.view.startStopButton.setStyleSheet("background-color: green; color:white")
        self.socket_server.close()
        self.send_continue_thread.quit()
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
            confirmation_msg = "Etes vous sur de vouloir supprimer des graphiques toutes " \
                               "les courbes affichées ? (" + str(len(self.curves_on_graph)) + \
                               (" courbes)" if len(self.curves_on_graph) > 1 else " courbe)")
            reply = QMessageBox.question(self.view, 'Attention !',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                DEBUG and print("=== acquisition_controller.py === SUPPRESION EN COURS")
                self.view.clear_graph()

                # Empty attribute
                self.curves_on_graph    = []

            else:
                DEBUG and print("=== acquisition_controller.py === ANNULATION")

    @pyqtSlot(name="save_curves_button_handler")
    def save_curves_button_handler(self):
        """
        Handler called when the save curves button from acquisition.py (saveButton) is clicked
        It basically retrieves the acquisition parameters, comments and the data given by Unity exe
        and save them into a file
        :return: Nothing
        """
        DEBUG and print('=== acquisition_controller.py === SAVE CURVES')

        # TODO CHECK USE
        data = self.yaw_pitch_roll

        self.selected_movement  = self.view.comboBox.currentText()
        self.angle              = self.view.text_angle.text()
        self.speed              = self.view.text_speed.text()
        self.nb_return          = self.view.text_nb_return.text()
        self.wait_time          = self.view.text_wait_time.text()
        self.comment            = self.view.text_area_comment.toPlainText()

        param = [self.selected_movement, self.angle, self.speed, self.nb_return, self.wait_time, self.comment]

        # Write Data into file with parameters and comment
        create_file_with_curves(self.last_name + "_" + self.first_name + "_" + self.age + "/", data, param)