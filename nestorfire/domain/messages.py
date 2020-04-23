from enum import Enum
from uuid import UUID
from typing import NamedTuple


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


@event
class FireEntryCreated(NamedTuple):
    fid: UUID
