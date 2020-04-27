from nestorfire.adapters.nasa_fire_datasource import NasaFireDatasource
from ..http import config

def import_fires():
    datasource = NasaFireDatasource()
    fires = datasource.get_data()
    for fire in fires:
        config.bus.handle(fire)
    