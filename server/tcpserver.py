import socket

from threading import Thread

from server.session_controller import SessionController


class TCPServer:
    def __init__(self, address: str, port: int):
        self.socket = socket.socket()
        self.socket.bind((address, port))

    def run(self):
        """
        Starts TCP server
        :return: none
        """
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            Thread(target=SessionController(connection).run).start()
