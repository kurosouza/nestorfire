from nestorfire.domain.models import FireEntry
from nestorfire.adapters.nasa_fire_datasource import NasaFireDatasource
from ..http import config

def import_fires():
    datasource = NasaFireDatasource()
    fires = datasource.get_data()
    [config.bus.handle(fire) for fire in fires]
    