import uuid
from nestorfire.domain.models import FireEntry

def test_can_create_fire_entry():
    lat = 54.2343
    lon = 22.3443
    fid = uuid.uuid4()
    fire_entry = FireEntry(fid = fid, lat = lat, lon = lon)
    assert fire_entry.lat == lat
    assert fire_entry.lon == lon
    assert fire_entry.fid == fid
    