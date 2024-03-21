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

    def __calculate_dwell_times(self, start=None, end=None, drivers=None):

        start_date, end_date = self.refine_dates(start, end)
        dwell_times = self.__dwell_times[(self.__dwell_times['date'] >= start_date) & (self.__dwell_times['date'] <= end_date)]

        if drivers is not None:
            dwell_times = dwell_times[dwell_times['deviceid'].isin(drivers)]

        grouped_df = dwell_times.groupby(['deviceid', 'bus_stop', 'direction']).agg(
            average_dwell_time=('dwell_time_in_seconds', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['deviceid', 'bus_stop_no', 'direction', 'average_dwell_time']

        grouped_df.sort_values(by=['direction', 'deviceid', 'bus_stop_no'], inplace=True)

        response = {
            "data": {
                "direction-1": [],
                "direction-2": []
            }
        }

        pre_device_id = None,
        pre_dir = None
        for index, row in grouped_df.iterrows():

            if pre_device_id == row['deviceid'] and pre_dir == row['direction']:
                obj = response['data'][f'direction-{int(row["direction"])}'][-1]
                new_one = False
            else:
                obj = {
                    "driverId": row['deviceid'],
                    "dwellTimes": []
                }
                new_one = True
            obj['dwellTimes'].append({
                "bus_stop_no": row['bus_stop_no'],
                "average_dwell_time": row['average_dwell_time']
            })
            if new_one:
                response['data'][f'direction-{int(row["direction"])}'].append(obj)

            # assigning previous
            pre_device_id = row['deviceid']
            pre_dir = row['direction']

        # all averages
        all_grouped = dwell_times.groupby(['bus_stop', 'direction']).agg(
            average_dwell_time=('dwell_time_in_seconds', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        all_grouped.columns = ['bus_stop_no', 'direction', 'average_dwell_time']

        all_grouped.sort_values(by=['direction', 'bus_stop_no'], inplace=True)

        # print(all_grouped)

        pre_dir = None
        for index, row in all_grouped.iterrows():
            if row['direction'] == pre_dir:
                obj = response['data'][f'direction-{int(row["direction"])}'][-1]
                new_one = False
            else:
                obj = {
                    "driverId": "all",
                    "dwellTimes": []
                }
                new_one = True

            obj['dwellTimes'].append({
                "bus_stop_no": row['bus_stop_no'],
                "average_dwell_time": row['average_dwell_time']
            })

            if new_one:
                response['data'][f'direction-{int(row["direction"])}'].append(obj)

            # assigning previous one
            pre_dir = row['direction']

        return response

    def get_dwell_times(self, start_date, end_date, drivers):

        if start_date or end_date or ((drivers is not None) and len(drivers) != 0):
            return self.__calculate_dwell_times(start_date, end_date, drivers)
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
