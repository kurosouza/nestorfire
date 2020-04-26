from nestorfire.adapters.nasa_fire_datasource import NasaFireDatasource;

def test_fire_data_reader():
    datasource = NasaFireDatasource()
    fires = datasource.get_data()    
    assert len(fires) > 0