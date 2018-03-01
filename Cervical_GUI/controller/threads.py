from PyQt5 import QtCore
from model.socket_server import *
import time

class SendContinueThread(QtCore.QThread):
    """
    SendContinueThread
    Thread that waits for the last stop of the sphere to send a "finishAcquisition" message
    """
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, socket_server_thread, wait_time, port_count, id, parent=None):
        """
        Constructor for the thread
        :param socket_server: The current socket server
        :param socket_server_thread:
        :param wait_time: The time to wait
        :param port_count: The port counter
        :param id: The id of this thread, allowing to ignore it if necessary
        :param parent: The parent thread
        """
        super(SendContinueThread, self).__init__(parent)
        self.send = True
        self.socket_server = socket_server
        self.socket_server_thread = socket_server_thread
        self.wait_time = wait_time
        self.id = id
        self.completion_message = str(self.id)
        self.port_count = port_count

    def run(self):
        """
        Run the thread
        :return: None
        """
        time.sleep(self.wait_time)
        #time.sleep(8)
        self.completeSignal.emit(self.completion_message)




class StartSocketServerThread(QtCore.QThread):
    """
    StartSocketServerThread
    Thread allowing to start a socket server and wait for the Unity app to connect
    """
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, port_count, parent=None):
        """
        Constructor
        :param socket_server: The current socket server
        :param port_count: The port counter to get the next port to use
        :param parent: The parent thread
        """
        super(StartSocketServerThread, self).__init__(parent)
        self.socket_server = socket_server
        self.completion_message = "server connected"
        self.port_count = port_count

    def run(self):
        """
        Start the socket server
        :return: None
        """
        self.socket_server.start(HOST, self.port_count)
        self.completeSignal.emit(self.completion_message)


class StartAcquisitionThread(QtCore.QThread):
    """
    StartAcquisitionThread
    Thread that sends the "startAcquisition" message
    """
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, conf, parent=None):
        """
        Constructor
        :param socket_server: the current socket server
        :param conf: The parameters for the acquisition in a dictionary
        :param parent: The parent thread
        """
        super(StartAcquisitionThread, self).__init__(parent)
        self.socket_server = socket_server
        self.conf = conf
        self.message = build_startAcquisition_message(conf)
        self.completion_message = "SENT: " + self.message

    def run(self):
        """
        Send the message
        :return: None
        """
        self.socket_server.send(self.message)
        self.completeSignal.emit(self.completion_message)


class StopAcquisitionThread(QtCore.QThread):
    """
    StopAcquisitionThread
    A thread that sends the "stopAcquisition" message
    """
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, parent=None):
        """
        Constructor
        :param socket_server: The current socket server
        :param parent: The parent thread
        """
        super(StopAcquisitionThread, self).__init__(parent)
        self.socket_server = socket_server
        self.message = "stopAcquisition"
        self.completion_message = "SENT: " + self.message

    def run(self):
        """
        Send the message
        :return: None
        """
        self.socket_server.send(self.message)
        self.completeSignal.emit(self.completion_message)