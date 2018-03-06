import socket

DEBUG = False


class PortCount:
    """
    PortCount
    Class that allows to increment the number of the port to use, using a new one each time
    """
    def __init__(self, starting_port):
        self.starting_port = starting_port
        self.port = starting_port
        self.ending_port = 51000

    def get_port(self):
        """
        Gets the next number of port
        :return: The number of the port to use
        """
        if self.port > self.ending_port:
            self.port = self.starting_port
        self.port = self.port + 1
        return self.port - 1

    def reset(self):
        """
        Resets the counter to the starting port
        :return: None
        """
        self.port = self.starting_port


class SocketServer:
    """
    SocketServer
    Class that represents a socket server, initializing it and allowing to send and receive message through the
    connection and close the connection
    """
    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port_counter):
        """
        Starts the socket server on the given host and port and waits for a client to connect
        :param host: The host of the server
        :param port_counter: The port of the server
        :return: None
        """
        self.port = port_counter.get_port()
        DEBUG and print("Starting server at {0}:{1}".format(host, self.port))
        self._s.bind((host, self.port))
        self._s.listen(1)
        DEBUG and print("Server started at {0}:{1}.".format(host, self.port))
        self._conn, self._addr = self._s.accept()
        DEBUG and print('Connected by {0}.'.format(self._addr[0], self._addr[1]))

    def send(self, message):
        """
        Send a message through the socket
        :param message: The string message to send
        :return: None
        """
        DEBUG and print("Send message: {0}".format(message))
        self._conn.send(message.encode("UTF-8"))

    def receive(self):
        """
        Receive a message through the socket
        :return: The string received message
        """
        while True:
            data = self._conn.recv(1024)
            if data: break
        DEBUG and print("Received message: " + data.decode('utf-8'))
        return data

    def detach(self):
        """
        Detaches the socket
        :return: None
        """
        self._conn.detach()

    def close(self):
        """
        Closes the socket
        :return: None
        """
        self._conn.close()


def build_startAcquisition_message(params):
    """
    Builds the startAcquisition message with the parameters and their values
    :param params:
    :return: the string message to send
    """
    message = "startAcquisition"

    for key in params:
        message += ",{0}:{1}".format(key, params[key])

    return message


def calculate_time_for_finish(params):
    """
    Calculates the time it takes to reach the last stop of the sphere before the end of the aquisition
    :param params: A dictionary with the parameters and their value
    :return: The float value of the calculated time.
    """
    return (4*float(params['sphereRoundTripNumber']) + 1)*(float(params['sphereLimitAngle'])/float(params['sphereSpeed'])) + float(params['sphereCountdownTime']) + (2*float(params['sphereRoundTripNumber'])*float(params['sphereWaitTime'])) - 2*float(params['sphereLimitAngle'])/float(params['sphereSpeed'])
