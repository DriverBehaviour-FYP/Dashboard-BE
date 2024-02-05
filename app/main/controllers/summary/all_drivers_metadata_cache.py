import pandas as pd

from app.main.loaders.data_loader import Data
import json


class AllDriverMetadata:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = self.__calculate_summary_metadata()
        self.__metadata_valid = True

    def __calculate_summary_metadata(self):

        data = {
            "success": True,
            'routes': self.__metadata_f_file['routes']
        }

        # calculate no of trips
        no_of_trips = len(self.__trips_data)
        data['no_of_trips'] = no_of_trips

        # calculate no of different drivers
        no_of_drivers = len(self.__gps_data['deviceid'].unique())
        data['no_of_drivers'] = no_of_drivers

        # data collection period
        data['data-collection-start-date'] = self.__trips_data['date'].min()
        data['data-collection-end-date'] = self.__trips_data['date'].max()
        data['data-collection-period'] = (pd.to_datetime(data['data-collection-end-date']) -
                                          pd.to_datetime(data['data-collection-start-date'])).days

        # calculate no of bus stops
        data['no_of_bus_stops'] = len(self.__bus_stops)

        return data

    def get_metadata(self):
        if self.__metadata_valid:
            return self.__data
        else:
            self.__data = self.__calculate_summary_metadata()
            self.__metadata_valid = True
            return self.__data

