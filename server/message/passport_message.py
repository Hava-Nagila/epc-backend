from server.message.session_message import SessionMessage


class PassportMessage(SessionMessage):
    def __init__(self, passport: dict):
        self.passport = passport
