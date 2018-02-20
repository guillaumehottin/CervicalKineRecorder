import socket


class SocketServer:

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self._s.bind((host, port))
        self._s.listen(1)
        print("Server started at {0} on port {1}.".format(host, port))
        self._conn, self._addr = self._s.accept()
        print('Connected by {0}.'.format(self._addr[0], self._addr[1]))

    def send(self, message):
        self._conn.send(message.encode("UTF-8"))

    def receive(self):
        while True:
            data = self._conn.recv(1024)
            if data: break
        return data

    def detach(self):
        self._conn.detach()

    def close(self):
        self._conn.close()


HOST = "localhost"
PORT = 50007

CONF = {"sphereSpeed":"10", "sphereLimitAngle":"20", "sphereWaitTime":"0.1",
        "sphereCountdownTime":"7", "sphereRoundTripNumber":"3"}


sock_serv = SocketServer()
sock_serv.start(HOST, PORT)

input("Press return to send 'startAcquisition'.")

message = "startAcquisition"

for key in CONF:
    message += ",{0}:{1}".format(key, CONF[key])

sock_serv.send(message)
sock_serv.close()

sock_serv = SocketServer()
sock_serv.start(HOST, PORT)

input("Press return to receive 'startAcquisitionAck'.")

print(sock_serv.receive())

res_input = input("Press 1 to send 'stopAcquisition'.")
if res_input == "1":
    sock_serv.send("stopAcquisition")
    sock_serv.close()

    sock_serv = SocketServer()
    sock_serv.start(HOST, PORT)
    input("Press return to receive 'stopAcquisitionAck'.")
    print(sock_serv.receive())
    sock_serv.close()
else:
    print(sock_serv.receive())
    sock_serv.close()
#print(repr(sock_serv.receive()))
#while True:
#    continue(


    
