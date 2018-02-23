import socket
import time
from PyQt5 import QtCore

from threading import Thread

class PortCount:

    def __init__(self, starting_port):
        self.starting_port = starting_port
        self.port = starting_port
        self.ending_port = 51000

    def get_port(self):
        if self.port > self.ending_port:
            self.port = self.starting_port
        self.port = self.port + 1
        return self.port - 1

    def reset(self):
        self.port = self.starting_port

class SocketServer:

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, host, port_counter):
        self.port = port_counter.get_port()
        print("Starting server at {0}:{1}".format(host, self.port))
        self._s.bind((host, self.port))
        self._s.listen(1)
        print("Server started at {0} on port {1}.".format(host, self.port))
        self._conn, self._addr = self._s.accept()
        print('Connected by {0}.'.format(self._addr[0], self._addr[1]))

    def send(self, message):
        print("SEND: {0}".format(message))
        self._conn.send(message.encode("UTF-8"))

    def receive(self):
        while True:
            data = self._conn.recv(1024)
            if data: break
        print("RECEIVE")
        return data


    def detach(self):
        self._conn.detach()


    def close(self):
        self._conn.close()



def build_startAcquisition_message(params):
    message = "startAcquisition"

    for key in params:
        message += ",{0}:{1}".format(key, params[key])

    return message


def calculate_time_for_finish(params):
    return (4*float(params['sphereRoundTripNumber']) + 1)*(float(params['sphereLimitAngle'])/float(params['sphereSpeed'])) + float(params['sphereCountdownTime']) + (2*float(params['sphereRoundTripNumber'])*float(params['sphereWaitTime'])) - 2*float(params['sphereLimitAngle'])/float(params['sphereSpeed'])
    


HOST = "localhost"
PORT = 50007