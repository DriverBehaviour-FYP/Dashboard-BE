import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE


class DriverDwellTimes:
    def __init__(self, version='10T'):
        self.__version = version
        self.__dwell_times = Data().get_dwell_times()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_driver_dwell_times(self, driver_id, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)
        dwell_times = self.__dwell_times[(self.__dwell_times['deviceid'] == driver_id) & (self.__dwell_times['date'] >= start_date) & (self.__dwell_times['date'] <= end_date)]

        grouped_df = dwell_times.groupby(['bus_stop']).agg(
            average_dwell_time=('dwell_time_in_seconds', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['bus_stop_no', 'average_dwell_time']

        return {
            "data": grouped_df.to_dict(orient='records'),
            "success": True
        }

    def get_driver_dwell_times(self, driver_id, start_date, end_date):
        return self.__calculate_driver_dwell_times(driver_id, start_date, end_date)

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date


