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

    def fetch(self, limit = None, offset = None):
        session = self.db.get_session()

        limit_fragment = ""
        offset_fragment = ""

        if  limit is not None:
            limit_fragment = f" limit {int(limit)}"
            print(f"got limit: {int(limit)}")

        if offset is not None:
            offset_fragment = f" offset {int(offset)}"
            print(f"got offset: {int(offset)}")
        
        query = session.execute(
            "SELECT fid, lat, lon, detection_date "
            + " FROM fires"
            + limit_fragment
            + offset_fragment
        )

        result = []
        for r in query.fetchall():
            # r = read_uuid(r, "fid") # Only enable for SQLite
            row = dict(r.items())
            result.append(row)

        return result


class FireEntryQueryBuilder:

    _q = "select f.fid, f.lat, f.lon from fires f, countries c " + \
        " where f.acq_time::date between date('{0}') and date('{1}')" + \
        " and ST_Contains(c.geom, f.geom) " + \
        " and 'c.ADMIN' = '{2}'"

    def __init__(self,db):
        self.db = db
        

    def fetch(self, start_date, end_date, country: str):
        query_str = str.format(self._q, start_date, end_date, country)
        session = self.db.get_session()

        print('Executing query: {0}'.format(query_str))
        
        query = session.execute(query_str)

        result = []
        for r in query.fetchall():
            row = dict(r.items())
            result.append(row)

        return result
        