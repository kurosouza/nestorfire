import abc
from collections import defaultdict
from uuid import UUID
from .models import FireEntry

from typing import List


class FireEntryNotFoundException(Exception):
    pass


class FireEntryLog(abc.ABC):
    @abc.abstractmethod
    def add(self, fire_entry: FireEntry) -> None:
        pass

    @abc.abstractmethod
    def _get(self, id: UUID) -> FireEntry:
        pass

    def get(self, id: UUID) -> FireEntry:
        fire_entry = self._get(id)
        if fire_entry is None:
            raise FireEntryNotFoundException()
        return fire_entry


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    @property
    @abc.abstractmethod
    def fires(self):
        pass


class UnitOfWorkManager(abc.ABC):
    @abc.abstractmethod
    def start(self) -> UnitOfWork:
        pass


class CommandAlreadySubscribedException(Exception):
    pass


class MessageBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def handle(self, msg):
        subscribers = self.subscribers[type(msg).__name__]
        for subscriber in subscribers:
            subscriber.handle(msg)

    def subscribe_to(self, msg, handler):
        subscribers = self.subscribers[msg.__name__]
        # We shouldn't be able to subscribe more
        # than one handler for a command
        if msg.is_cmd and len(subscribers) > 0:
            raise CommandAlreadySubscribedException(msg.__name__)
        subscribers.append(handler)


class FireEntryViewBuilder:
    @abc.abstractmethod
    def fetch(self, id):
        pass


class FireDataSource(abc.ABC):

    @abc.abstractmethod
    def get_data(self) -> list:
        pass
