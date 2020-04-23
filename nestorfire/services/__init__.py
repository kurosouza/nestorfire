
from nestorfire.domain.models import FireEntry
from nestorfire.domain.ports import UnitOfWorkManager, FireEntryViewBuilder

class CreateFireEntryHandler:

    def __init__(self, uowm: UnitOfWorkManager):
        self.uowm = uowm

    def handle(self, cmd):
        fire_entry = FireEntry(cmd.fid, cmd.lat, cmd.lon)
        with self.uowm.start() as tx:
            tx.fires.add(fire_entry)
            tx.commit()
