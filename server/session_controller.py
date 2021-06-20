import logging
import socket
from typing import Final

from server.message import PassportMessage
from server.session import Session
from server.task import Task


class SessionController:
    DEFAULT_DATA_PACKET_LENGTH: Final = 512

    def __init__(self, connection: socket):
        self.logger = logging.getLogger("root")
        self.connection = connection
        self.session = Session()
        self.session.add_callback(self.__session_callback)

    def __listen(self):
        data = self.__receive(1)
        self.session.push_task(Task(data))

    def __receive(self, length: int):
        result = b""
        remaining_length = length
        while remaining_length > 0:
            result += self.connection.recvfrom(
                self.DEFAULT_DATA_PACKET_LENGTH
                if remaining_length > self.DEFAULT_DATA_PACKET_LENGTH
                else remaining_length
            )[0]
            remaining_length = length - len(result)
        return result

    def __session_callback(self, message: PassportMessage):
        self.connection.send(int(
            message.passport['taxonomy'] * 10 ** 6
        ).to_bytes(4, byteorder='little'))

    def run(self):
        """
        Starts client listening loop
        :return: none
        """
        try:
            while True:
                self.__listen()
        except (ConnectionResetError, ConnectionAbortedError):
            self.session.close()
            return
