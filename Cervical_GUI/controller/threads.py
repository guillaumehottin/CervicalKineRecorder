from PyQt5 import QtCore
from model.socket_server import *


class SendContinueThread(QtCore.QThread):
    # Signals to relay thread progress to the main GUI thread
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, socket_server_thread, wait_time, port_count, id, parent=None):
        super(SendContinueThread, self).__init__(parent)
        # You can change variables defined here after initialization - but before calling start()
        self.send = True
        self.socket_server = socket_server
        self.socket_server_thread = socket_server_thread
        self.wait_time = wait_time
        self.id = id
        self.completion_message = str(self.id)
        self.port_count = port_count

    def run(self):
        time.sleep(self.wait_time)
        #time.sleep(8)
        self.completeSignal.emit(self.completion_message)




class StartSocketServerThread(QtCore.QThread):
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, port_count, parent=None):
        super(StartSocketServerThread, self).__init__(parent)
        # You can change variables defined here after initialization - but before calling start()
        self.socket_server = socket_server
        self.completion_message = "server connected"
        self.port_count = port_count

    def run(self):
        self.socket_server.start(HOST, self.port_count)
        self.completeSignal.emit(self.completion_message)


class StartAcquisitionThread(QtCore.QThread):
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, conf, parent=None):
        super(StartAcquisitionThread, self).__init__(parent)
        # You can change variables defined here after initialization - but before calling start()
        self.socket_server = socket_server
        self.conf = conf
        self.message = build_startAcquisition_message(conf)
        self.completion_message = "SENT: " + self.message

    def run(self):
        self.socket_server.send(self.message)
        self.completeSignal.emit(self.completion_message)


class StopAcquisitionThread(QtCore.QThread):
    completeSignal = QtCore.pyqtSignal(str)

    def __init__(self, socket_server, parent=None):
        super(StopAcquisitionThread, self).__init__(parent)
        # You can change variables defined here after initialization - but before calling start()
        self.socket_server = socket_server
        self.message = "stopAcquisition"
        self.completion_message = "SENT: " + self.message

    def run(self):
        self.socket_server.send(self.message)
        self.completeSignal.emit(self.completion_message)