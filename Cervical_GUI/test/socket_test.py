# -*- coding: utf-8 -*-

import socket

HOST = "localhost"
PORT = 8080

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))

while True:
        print("LET'S LOOP")
        socket.listen(5)
        client, address = socket.accept()
        print("{} connected".format(address))

        response = client.recv(255)
        if response != "":
                print(response)

print("Close")
client.close()
stock.close()