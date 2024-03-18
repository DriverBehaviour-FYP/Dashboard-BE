import pandas as pd
from app.main.loaders.data_loader import Data


class DriverSpeedController:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__common_metadata = Data().get_common_metadata()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_driver_speed_percentages(self, driver_id, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)
        gps_data = self.__gps_data[(self.__gps_data['deviceid'] == driver_id) & (self.__gps_data['date'] >= start_date) & (self.__gps_data['date'] <= end_date)]

        gps_data = gps_data[gps_data['speed'] != 0]

        response = {
            "success": True,
            "data":{
            "total-length": len(gps_data),
            'higher-than-3rd-quantile': len(gps_data[gps_data['speed'] >= self.__common_metadata['3rd-quantile']]),
            'lower-than-1st-quantile': len(gps_data[gps_data['speed'] <= self.__common_metadata['1st-quantile']]),
        }}
        response["data"]['between'] = response["data"]['total-length'] - response["data"]['higher-than-3rd-quantile'] - response["data"]['lower-than-1st-quantile']

        return response

    def get_speed_percentages(self, driver_id, start_date, end_date):
        return self.__calculate_driver_speed_percentages(driver_id, start_date, end_date)

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date


