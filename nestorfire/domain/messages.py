from enum import Enum
from uuid import UUID
from typing import NamedTuple
from datetime import datetime


def event(cls):

    setattr(cls, "is_cmd", property(lambda x: getattr(x, "is_cmd", False)))
    setattr(cls, "is_event", property(lambda x: getattr(x, "is_event", True)))
    setattr(cls, "id", property(lambda x: getattr(x, "id", None)))

    return cls


def command(cls):

    setattr(cls, "is_cmd", property(lambda x: getattr(x, "is_cmd", True)))
    setattr(cls, "is_event", property(lambda x: getattr(x, "is_event", False)))
    setattr(cls, "id", property(lambda x: getattr(x, "id", None)))

    return cls


@command
class AddFireEntry(NamedTuple):
    fid: UUID
    lat: float
    lon: float
    created_on: str
    acq_time: datetime


@command
class RemoveFireEntry(NamedTuple):
    fid: UUID


@event
class FireEntryCreated(NamedTuple):
    fid: UUID


@event
class FireEntryRemoved(NamedTuple):
    fid: UUID
