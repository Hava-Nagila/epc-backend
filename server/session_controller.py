import logging
import socket
from typing import Final

from server.message.session_message import SessionMessage
from server.network import Header, Event
from server.session import Session
from server.task import Task


class SessionController:
    DEFAULT_DATA_PACKET_LENGTH: Final = 512

    def __init__(self, connection: socket):
        self.logger = logging.getLogger('root')
        self.connection = connection
        self.session = Session()
        self.session.add_callback(self.__session_callback)

    def __listen(self):
        header = Header(self.__receive(Header.LENGTH))
        data = self.__receive(header.data_length)

        if header.event == Event.INIT_SESSION:
            pass
        elif header.event == Event.BUS_DETECTION:
            image = Data.decode_image(data)
            self.session.push_task(Task(Event.BUS_DETECTION, image))
        elif header.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
            image = Data.decode_image(data)
            self.session.push_task(Task(Event.BUS_ROUTE_NUMBER_RECOGNITION, image))

    def __receive(self, length: int):
        result = b''
        remaining_length = length
        while remaining_length > 0:
            result += self.connection.recvfrom(self.DEFAULT_DATA_PACKET_LENGTH
                                               if remaining_length > self.DEFAULT_DATA_PACKET_LENGTH
                                               else remaining_length)[0]
            remaining_length = length - len(result)
        return result

    def __answer(self, header: Header, data: bytes = None):
        try:
            if data is not None:
                self.connection.send(header.to_bytes() + data)
                result = Data.decode_bus_boxes(data)
                self.logger.info('RESULT RESPONSE: ' + str(result))
            else:
                self.connection.send(header.to_bytes())
        except (ConnectionResetError, ConnectionAbortedError):
            return

    # Session message handlers =========================================================================================
    def __session_callback(self, message: SessionMessage):
        if message.event == Event.BUS_DETECTION or message.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
            data = Data.encode_bus_boxes(message.bus_boxes)
            header = Header(event=message.event, token=0,
                            data_length=len(data))  # TODO: Add token
            self.__answer(header, data)

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
