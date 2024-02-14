import pandas as pd
from datetime import datetime as d
from app.main.loaders.data_loader import Data


class AllDriverMetadata:
    def __init__(self, version='1000M'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = self.__calculate_summary_metadata()
        self.__metadata_valid = True

    def __calculate_summary_metadata(self, start=None, end=None):
        start_date, end_date = self.refine_dates(start, end)
        trips_data = self.__trips_data[(self.__trips_data['date'] >= start_date) & (self.__trips_data['date'] <= end_date)]
        gps_data = self.__gps_data[(self.__gps_data['date'] >= start_date) & (self.__gps_data['date'] <= end_date)]

        data = {
            "success": True,
            'routes': self.__metadata_f_file['routes']
        }

        # calculate no of trips
        no_of_trips = len(trips_data)
        data['no-of-trips'] = no_of_trips

        # calculate no of different drivers
        no_of_drivers = len(gps_data['deviceid'].unique())
        data['no_of_drivers'] = no_of_drivers

        # data collection period
        data['data-collection-start-date'] = self.__metadata_f_file['data-collection-start-date']
        data['data-collection-end-date'] = self.__metadata_f_file['data-collection-end-date']
        data['data-collection-period'] = (pd.to_datetime(data['data-collection-end-date']) -
                                          pd.to_datetime(data['data-collection-start-date'])).days

        # calculate no of bus stops
        data['no-of-bus-stops'] = len(self.__bus_stops)

        data['selected-start-date'] = start_date.strftime("%Y-%m-%d")
        data['selected-end-date'] = end_date.strftime("%Y-%m-%d")

        return data

    def get_metadata(self, start_date, end_date):
        if start_date or end_date:
            return self.__calculate_summary_metadata(start_date, end_date)
        if self.__metadata_valid:
            return self.__data
        else:
            self.__data = self.__calculate_summary_metadata()
            self.__metadata_valid = True
            return self.__data

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date

