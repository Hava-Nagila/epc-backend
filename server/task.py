import time


class Task:
    def __init__(self, data: bytes = None):
        self.data = int.from_bytes(data, byteorder='little')
        self.creation_time = time.time()
