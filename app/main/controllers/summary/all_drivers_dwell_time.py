from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE
import pandas as pd


class AllDriverDwellTime:
    def __init__(self, version='1000M'):
        self.__version = version
        self.__dwell_times = Data().get_dwell_times()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = None
        self.__cache_valid = False

    def __calculate_dwell_times(self, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)
        dwell_times = self.__dwell_times[(self.__dwell_times['date'] >= start_date) & (self.__dwell_times['date'] <= end_date)]

        grouped_df = dwell_times.groupby(['deviceid', 'bus_stop']).agg(
            average_dwell_time=('dwell_time_in_seconds', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['deviceid', 'bus_stop_no', 'average_dwell_time']

        return {"data": grouped_df.to_dict(orient='records')}

    def get_dwell_times(self, start_date, end_date):

        if start_date or end_date:
            return self.__calculate_dwell_times(start_date, end_date)
        if self.__cache_valid:
            return self.__data
        else:
            self.__data = self.__calculate_dwell_times()
            self.__cache_valid = True
            return self.__data

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date
