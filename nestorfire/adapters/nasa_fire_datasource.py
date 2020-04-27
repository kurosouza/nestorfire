from nestorfire.domain.ports import FireDataSource
from nestorfire.domain.messages import AddFireEntry
import requests
import csv
import uuid
import datetime
from typing import List

datasource_csv_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_24h.csv"

class NasaFireDatasource(FireDataSource):

    def get_data(self):

        fire_data_file = requests.get(datasource_csv_url)
        with open('fire-data.csv', 'wb') as f:
            f.write(fire_data_file.content)
        fire_list = []
        read_count = 0
        with open('fire-data.csv', 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                if read_count > 0:
                    lat = row[0]
                    lon = row[1]
                    print("Found fire entry: lat: {}, lon: {}".format(lat, lon))
                    fid = uuid.uuid4()
                    fire_entry = AddFireEntry(fid = fid, lat = lat, lon = lon, created_on = str(datetime.datetime.now()))
                    fire_list.append(fire_entry)
                read_count += 1            

        return fire_list