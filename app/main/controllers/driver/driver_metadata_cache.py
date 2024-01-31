import pandas as pd
from app.main.loaders.data_loader import Data
import json


class DriverMetadata:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = dict()
        self.__metadata_valid = True

    def __calculate_driver_metadata(self, driver_id):
        temp_df = self.__trips_data[self.__trips_data['deviceid'] == driver_id]

        data = {
            "driver_id": driver_id,
            "no_of_trips": len(temp_df),
            "routes": self.__metadata_f_file['routes'],
            "data-collection-start-date": temp_df['date'].min(),
            "data-collection-end-date": temp_df['date'].max(),
            "data-collection-period": (pd.to_datetime(temp_df['date'].max()) - pd.to_datetime(temp_df['date'].min())).days
        }
        self.__data[driver_id] = data

        return data

    def get_driver_metadata(self, driver_id):
        metadata = self.__data.get(driver_id)
        if metadata is None:
            return self.__calculate_driver_metadata(driver_id)
        else:
            return metadata

