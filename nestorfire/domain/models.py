import abc
import datetime
from uuid import UUID
from .messages import FireEntryCreated


class FireEntry:
    def __init__(self, fid: UUID, lat: float, lon: float):
        self.fid = fid
        self.lat = lat
        self.lon = lon
        self.detection_date = datetime.datetime.now()
