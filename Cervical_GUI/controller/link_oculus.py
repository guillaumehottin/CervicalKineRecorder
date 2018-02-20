# -*- coding: utf-8 -*-

import socket

HOST        = "localhost"
PORT_WRITE  = 8080
PORT_READ   = 6667


class LinkOculus:

    def __init__(self):
        self.socket_write = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_write.connect((HOST, PORT_WRITE))

        self.socket_read = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket_read.bind((HOST, PORT_READ))

    def start_acquisition(self, movement, angle, speed, nb_return, time_limit):
        print("SEND startAcquisition")
        self.socket_write.send(b'startAcquisition')
        #acquisition_info = [movement, angle, speed, nb_return, time_limit]
        #server_socket.send(acquisition_info)
        # TODO RECEIVE ANSWER FROM OCULUS
        # TODO SEND ALL INFO

    def stop_acquisition(self):
        print("SEND stopAcquisition")
        self.socket_write.send(b'stopAcquisition')




