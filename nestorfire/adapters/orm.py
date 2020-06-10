import collections
import logging
import uuid

import sqlalchemy
from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String,
    Integer,
    Float,
    Text,
    ForeignKey,
    create_engine,
    event,
)
from geoalchemy2 import Geometry

from sqlalchemy.orm import mapper, scoped_session, sessionmaker, composite, relationship
import sqlalchemy.exc
import sqlalchemy.orm.exc

from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy_utils.types.uuid import UUIDType

from nestorfire.domain.models import FireEntry
from nestorfire.domain.ports import (
    FireEntryLog,
    UnitOfWork,
    UnitOfWorkManager,
)


class SqlAlchemyUnitOfWorkManager(UnitOfWorkManager):
    def __init__(self, session_maker, bus):
        self.session_maker = session_maker
        self.bus = bus

    def start(self):
        return SqlAlchemyUnitOfWork(self.session_maker, self.bus)


class FireEntryRepository(FireEntryLog):
    def __init__(self, session):
        self._session = session

    def add(self, fire_entry: FireEntry) -> None:
        self._session.add(fire_entry)

    def _get(self, fid) -> FireEntry:
        return self._session.query(FireEntry).filter_by(fid=fid).first()


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, sessionfactory, bus):
        self.sessionfactory = sessionfactory
        self.bus = bus
        event.listen(self.sessionfactory, "after_flush", self.gather_events)
        event.listen(self.sessionfactory, "loaded_as_persistent", self.setup_events)

    def __enter__(self):
        self.session = self.sessionfactory()
        self.flushed_events = []
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()
        self.publish_events()

    def commit(self):
        self.session.flush()
        self.session.commit()

    def rollback(self):
        self.flushed_events = []
        self.session.rollback()

    def setup_events(self, session, entity):
        entity.events = []

    def gather_events(self, session, ctx):
        flushed_objects = [e for e in session.new] + [e for e in session.dirty]
        for e in flushed_objects:
            try:
                self.flushed_events += e.events
            except AttributeError:
                pass

    def publish_events(self):
        for e in self.flushed_events:
            self.bus.handle(e)

    @property
    def fires(self):
        return FireEntryRepository(self.session)


class SqlAlchemy:
    def __init__(self, uri):
        self.engine = create_engine(uri, )
        self._session_maker = scoped_session(sessionmaker(self.engine),)

    @property
    def unit_of_work_manager(self):
        return SqlAlchemyUnitOfWorkManager(self._session_maker, self.bus)

    def recreate_schema(self):
        drop_database(self.engine.url)
        self.create_schema()

    def create_schema(self):
        create_database(self.engine.url)
        self.metadata.create_all()

    def create_tables(self):
        self.metadata.create_all()

    def drop_tables(self):
        self.metadata.drop_all()        

    def drop_schema(self):
        drop_database(self.engine.url)

    def get_session(self):
        return self._session_maker()

    def associate_message_bus(self, bus):
        self.bus = bus

    def configure_mappings(self):
        self.metadata = MetaData(self.engine)

        fires = Table("fires", self.metadata,
            Column("fid", UUIDType, primary_key = True),
            Column("lat", Float),
            Column("lon", Float),
            Column("detection_date", String(50)),
            Column("geom", Geometry("Point"))
        )

        mapper(FireEntry, fires, properties = {
            "fid": fires.c.fid,
            "lat": fires.c.lat,
            "lon": fires.c.lon,
            "detection_date": fires.c.detection_date,
            "geom": fires.c.geom
        })


class SqlAlchemySessionContext:
    def __init__(self, session_maker):
        self._session_maker = session_maker

    def __enter__(self):
        self._session = self._session_maker()

    def __exit__(self, type, value, traceback):
        self._session_maker.remove()
