from nestorfire.domain.ports import FireDataSource
from nestorfire.domain.models import FireEntry
import requests
import csv
import uuid
from typing import List

datasource_csv_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_24h.csv"

class NasaFireDatasource(FireDataSource):

    def get_data(self):

        fire_data_file = requests.get(datasource_csv_url)
        with open('fire-data.csv', 'wb') as f:
            f.write(fire_data_file.content)
        fire_list = []
        with open('fire-data.csv', 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                print("Found fire entry: lat: {}, lon: {}".format(row[0], row[1]))
                fid = uuid.uuid4()
                fire_entry = FireEntry(fid = fid, lat = row[0], lon = row[1])
                fire_list.append(fire_entry)            

        return fire_list