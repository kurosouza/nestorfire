import collections
import uuid

# This little helper function converts the binary data
# We store in Sqlite back to a uuid.
# Ordinarily I use postgres, which has a native UniqueID
# type, so this manual unmarshalling isn't necessary


def read_uuid(record, column):
    record = dict(record)
    bytes_val = record[column]
    uuid_val = uuid.UUID(bytes=bytes_val)
    record[column] = uuid_val
    return record


class FireEntryViewBuilder:

    _q = """SELECT detection_date,
                 lat,
                 lon
            FROM fires
            WHERE fid = :id"""

    def __init__(self, db):
        self.db = db

    def fetch(self, id):
        session = self.db.get_session()
        result = session.execute(self._q, {"id": id.bytes})
        record = result.fetchone()
        return dict(record)


class FireEntryListBuilder:

    _q = """SELECT fid,
                 lat,
                 lon,
                 detection_date
            FROM fires"""

    def __init__(self, db):
        self.db = db

    def fetch(self):
        session = self.db.get_session()
        query = session.execute(
            "SELECT fid, lat, lon, detection_date "
            + " FROM fires"
        )

        result = []
        for r in query.fetchall():
            r = read_uuid(r, "fid")
            result.append(r)

        return result
