import logging

from ..orm import SqlAlchemy
from ..views import FireEntryListBuilder, FireEntryViewBuilder, FireEntryQueryBuilder
from nestorfire.services import (
    CreateFireEntryHandler,
)

import nestorfire.domain.messages as msg
from nestorfire.domain.ports import MessageBus

import os
# from dotenv import load_dotenv

# load_dotenv()
db_url = os.environ.get("DB_URL")

db = SqlAlchemy(db_url)
db.configure_mappings()
# db.drop_tables()
db.create_tables()

bus = MessageBus()
db.associate_message_bus(bus)

fireentry_view_builder = FireEntryViewBuilder(db)
fireentry_list_builder = FireEntryListBuilder(db)
fireentry_query_builder = FireEntryQueryBuilder(db)

create_fireentry = CreateFireEntryHandler(db.unit_of_work_manager)

bus.subscribe_to(msg.AddFireEntry, create_fireentry)
