import pandas as pd
from app.main.loaders.data_loader import Data


class DriverSpeedController:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__common_metadata = Data().get_common_metadata()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_per_direction(self, driver_id, start_date, end_date, direction=None, trips=None):
        gps_data = self.__gps_data[
            (self.__gps_data['deviceid'] == driver_id) & (self.__gps_data['date'] >= start_date) & (
                    self.__gps_data['date'] <= end_date)]

        if direction is not None:
            gps_data = gps_data[gps_data['direction'] == direction]

        if (trips is not None) and len(trips) != 0:
            gps_data = gps_data[gps_data['trip_id'].isin(trips)]

        gps_data = gps_data[gps_data['speed'] != 0]

        response = {
            "total-length": len(gps_data),
            'higher-than-3rd-quantile': len(gps_data[gps_data['speed'] >= self.__common_metadata['3rd-quantile']]),
            'lower-than-1st-quantile': len(gps_data[gps_data['speed'] <= self.__common_metadata['1st-quantile']]),
        }
        response['between'] = response['total-length'] - response['higher-than-3rd-quantile'] - \
                              response['lower-than-1st-quantile']
        return response

    def __calculate_driver_speed_percentages(self, driver_id, start=None, end=None, trips=None):
        start_date, end_date = self.refine_dates(start, end)

        response = {
            "success": True,
            "data": {
                "direction-all": self.__calculate_per_direction(driver_id, start_date, end_date, direction=None, trips=trips),
                "direction-1": self.__calculate_per_direction(driver_id, start_date, end_date, direction=1, trips=trips),
                "direction-2": self.__calculate_per_direction(driver_id, start_date, end_date, direction=2, trips=trips),

            }}

        return response

    def get_speed_percentages(self, driver_id, start_date, end_date, trips):
        return self.__calculate_driver_speed_percentages(driver_id, start_date, end_date, trips)

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date
