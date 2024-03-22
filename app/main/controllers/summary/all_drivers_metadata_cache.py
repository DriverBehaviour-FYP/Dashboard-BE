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

    def __calculate_summary_metadata(self, start=None, end=None, drivers=None):
        start_date, end_date = self.refine_dates(start, end)
        trips_data = self.__trips_data[
            (self.__trips_data['date'] >= start_date) & (self.__trips_data['date'] <= end_date)]
        gps_data = self.__gps_data[(self.__gps_data['date'] >= start_date) & (self.__gps_data['date'] <= end_date)]

        if drivers is not None:
            trips_data = trips_data[trips_data['deviceid'].isin(drivers)]
            gps_data = gps_data[gps_data['deviceid'].isin(drivers)]

        data = {'routes': self.__metadata_f_file['routes'],
                'direction-all': {
                    "no-of-trips": len(trips_data),
                    'no-of-bus-stops': len(self.__bus_stops)
                }, 'direction-1': {
                "no-of-trips": len(trips_data[trips_data['direction'] == 1]),
                'no-of-bus-stops': len(self.__bus_stops[self.__bus_stops['stop_id'] < 200])
            }, 'direction-2': {
                "no-of-trips": len(trips_data[trips_data['direction'] == 2]),
                'no-of-bus-stops': len(self.__bus_stops[self.__bus_stops['stop_id'] >= 200])
            }}

        # calculate no of trips

        # calculate no of different drivers
        no_of_drivers = len(gps_data['deviceid'].unique())
        data['no-of-drivers'] = no_of_drivers

        # data collection period
        data['data-collection-start-date'] = self.__metadata_f_file['data-collection-start-date']
        data['data-collection-end-date'] = self.__metadata_f_file['data-collection-end-date']
        data['data-collection-period'] = (pd.to_datetime(data['data-collection-end-date']) -
                                          pd.to_datetime(data['data-collection-start-date'])).days

        data['selected-start-date'] = start_date.strftime("%Y-%m-%d")
        data['selected-end-date'] = end_date.strftime("%Y-%m-%d")

        return data

    def get_metadata(self, start_date, end_date, drivers):
        if start_date or end_date or ((drivers is not None) and len(drivers) != 0):
            return self.__calculate_summary_metadata(start_date, end_date, drivers)
        if self.__metadata_valid:
            return self.__data
        else:
            self.__data = self.__calculate_summary_metadata()
            self.__metadata_valid = True
            return self.__data

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date

    def get_all_drivers(self, start, end):
        start_date, end_date = self.refine_dates(start, end)

        trips_data = self.__trips_data[
            (self.__trips_data['date'] >= start_date) & (self.__trips_data['date'] <= end_date)]

        return trips_data['deviceid'].unique()
