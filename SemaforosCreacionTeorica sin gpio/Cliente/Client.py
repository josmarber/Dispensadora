__author__ = 'Chema'
import socket


class Client:
    """Class for a client"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def command(self):
        while True:
            command = input('As tu peio miarma: ')
            self.client.send(command.encode())
            reply = self.client.recv(1024).decode()

            print(reply)