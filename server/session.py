import logging
import threading
import time
from collections import deque
from typing import Final

from common.event.publisher import Publisher


class Session(Publisher):
    TASKS_DEQUE_MAXIMUM_LENGTH: Final = 8
    TASK_MAX_TIME_DELAY: Final = 2.0

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('root')

        self.__close_flag = False

        self.__tasks = deque(maxlen=self.TASKS_DEQUE_MAXIMUM_LENGTH)
        self.__tasks_semaphore = threading.Semaphore(0)
        self.__tasks_mutex = threading.Lock()
        self.__thread = threading.Thread(target=self.__run)
        self.logger.info('Session initialized')

        self.__thread.start()

    def __run(self):
        """
        Starts session
        :return: none
        """
        while True:
            if self.__close_flag:
                return
            self.__remove_old_tasks()
            self.__tasks_semaphore.acquire()
            try:
                task = self.__tasks.pop()
            except IndexError:  # TODO: Remove this if never happens
                self.logger.error('Session synchronisation error')
                continue
            if task.event == Event.BUS_DETECTION:
                self.__run_bus_detection_pipeline(task.image)
            elif task.event == Event.BUS_ROUTE_NUMBER_RECOGNITION:
                self.__run_bus_route_number_recognition_pipeline(task.image)
            elif task.event == Event.BUS_DOOR_DETECTION:
                self.__run_bus_route_number_recognition_pipeline(task.image)

    def __remove_old_tasks(self):
        self.__tasks_mutex.acquire()
        while self.__tasks and time.time() - self.__tasks[
            0].creation_time > self.TASK_MAX_TIME_DELAY:
            self.__tasks_semaphore.acquire()
            self.__tasks.popleft()
        self.__tasks_mutex.release()

    def push_task(self, task: Task):
        """
        Pushes task in queue
        :param task: Task to do
        :return: none
        """
        self.logger.info('Push task -> ' + str(task.event))
        self.__tasks_mutex.acquire()
        is_need_to_semaphore_release = False
        if len(self.__tasks) < 8:
            is_need_to_semaphore_release = True
        self.__tasks.append(task)
        if is_need_to_semaphore_release:
            self.__tasks_semaphore.release()
        self.__tasks_mutex.release()

    def close(self):
        self.__close_flag = True
