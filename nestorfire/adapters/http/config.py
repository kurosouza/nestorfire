import logging

from ..orm import SqlAlchemy
from ..views import FireEntryListBuilder, FireEntryViewBuilder
from nestorfire.services import (
    CreateFireEntryHandler,
)

import nestorfire.domain.messages as msg
from nestorfire.domain.ports import MessageBus

db = SqlAlchemy("sqlite:///nestorfire.db")
db.configure_mappings()
db.create_schema()

bus = MessageBus()
db.associate_message_bus(bus)

fireentry_view_builder = FireEntryViewBuilder(db)
fireentry_list_builder = FireEntryListBuilder(db)

create_fireentry = CreateFireEntryHandler(db.unit_of_work_manager)

bus.subscribe_to(msg.AddFireEntry, create_fireentry)
