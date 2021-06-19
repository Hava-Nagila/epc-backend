from typing import List

from server.message.session_message import SessionMessage
from server.network import Event


class BusBoxMessage(SessionMessage):
    def __init__(self, event: Event, bus_boxes: List[BusBox]):
        """
        Initialize BusBoxMessage
        :param event: Message event
        :param bus_boxes: List of bus boxes
        """
        super().__init__(event)
        self.bus_boxes: List[BusBox] = bus_boxes
