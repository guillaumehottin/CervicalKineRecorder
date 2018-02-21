import socket
import time
from threading import Thread

class SocketServer:

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self, host, port):
        print("bind")
        self._s.bind((host, port))
        print("listen")
        self._s.listen(1)
        print("Server started at {0} on port {1}.".format(host, port))
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


class SendContinue(Thread):

    def __init__(self, socket_server, wait_time):
        Thread.__init__(self)
        self.send = False
        self.socket_server = socket_server
        self.wait_time = wait_time

    def run(self):
        print("run thread")
        time.sleep(calculate_time_for_finish(CONF))
        print("end sleep")

        if self.send:
            print("send")
            self.socket_server.send("finishAcquisition")
            self.socket_server.close()

            self.socket_server = SocketServer()
            self.socket_server.start(HOST, PORT)


def build_startAcquisition_message(params):
    message = "startAcquisition"

    for key in params:
        message += ",{0}:{1}".format(key, params[key])

    return message


def calculate_time_for_finish(params):
    return (4*float(params['sphereRoundTripNumber']) + 1)*(float(params['sphereLimitAngle'])/float(params['sphereSpeed'])) + float(params['sphereCountdownTime']) + (2*float(params['sphereRoundTripNumber'])*float(params['sphereWaitTime'])) - 2*float(params['sphereLimitAngle'])/float(params['sphereSpeed'])
    


HOST = "localhost"
PORT = 50007

CONF = {"sphereSpeed":"20", "sphereLimitAngle":"40", "sphereWaitTime":"0.2",
        "sphereCountdownTime":"3", "sphereRoundTripNumber":"4",
        "profileName":"salut", "sphereGreenToYellowAngle":"0.1", "sphereYellowToRedAngle":"0.2"}

# for i in range(3):
#     print("\n======BEGIN=====")
#     sock_serv = SocketServer()
#     sock_serv.start(HOST, PORT)
#
#     input("Press return to send 'startAcquisition'.")
#
#     message = build_startAcquisition_message(CONF)
#
#     sock_serv.send(message)
#     sock_serv.close()
#
#     sock_serv = SocketServer()
#     sock_serv.start(HOST, PORT)
#
#     print(sock_serv.receive())
#
#     print(calculate_time_for_finish(CONF))
#
#     time.sleep(calculate_time_for_finish(CONF))
#     sock_serv.send("finishAcquisition")
#     sock_serv.close()
#
#     sock_serv = SocketServer()
#     sock_serv.start(HOST, PORT)
#
#     print(sock_serv.receive())
#     sock_serv.close()

##    res_input = input("Press s to send 'stopAcquisition', c send 'finishAcquisition'.")
##    if res_input == "s":
##        sock_serv.send("stopAcquisition")
##        sock_serv.close()
##
##        sock_serv = SocketServer()
##        sock_serv.start(HOST, PORT)
##
##        print(sock_serv.receive())
##        sock_serv.close()
##    elif res_input == "c":
##        sock_serv.send("finishAcquisition")
##        sock_serv.close()
##        
##        sock_serv = SocketServer()
##        sock_serv.start(HOST, PORT)
##        
##        print(sock_serv.receive())
##        sock_serv.close()
#print(repr(sock_serv.receive()))
#while True:
#    continue(


    
