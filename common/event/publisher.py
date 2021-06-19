from common.event.message import Message


class Publisher:
    def __init__(self):
        self.__callbacks = []

    def add_callback(self, callback):
        """
        Subscribe to publisher events, ask him to run callback
        :param callback: callback function
        :return none
        """
        self.__callbacks.append(callback)

    def broadcast(self, message: Message):
        """
        Runs listeners callbacks
        :param message:
        :return none
        """
        for callback in self.__callbacks:
            callback(message)  # TODO: Run callback at new thread
