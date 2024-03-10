from app.main.loaders.data_loader import Data
import pandas as pd


class AllDriverSpeed:
    def __init__(self, version='1000M'):
        self.__version = version
        self.__speed_at_zones = Data().get_speed_at_zones()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = None
        self.__cache_valid = False

    def __calculate_speed_at_zones(self, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)
        speed_at_zones = self.__speed_at_zones[(self.__speed_at_zones['date'] >= start_date) & (self.__speed_at_zones['date'] <= end_date)]

        speed_at_zones = speed_at_zones[speed_at_zones['zone']%1 != 0]

        grouped_df = speed_at_zones.groupby(['deviceid', 'zone', 'direction']).agg(
            average_dwell_time=('speed', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['deviceid', 'zone', 'direction', 'average_speed']

        grouped_df.sort_values(by=['direction', 'deviceid', 'zone'], inplace=True)

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
                    "speeds": []
                }
                new_one = True
            obj['speeds'].append({
                "zone": row['zone'],
                "average_speed": row['average_speed']
            })
            if new_one:
                response['data'][f'direction-{int(row["direction"])}'].append(obj)

            # assigning previous
            pre_device_id = row['deviceid']
            pre_dir = row['direction']

        # all averages
        all_grouped = speed_at_zones.groupby(['zone', 'direction']).agg(
            average_dwell_time=('speed', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        all_grouped.columns = ['zone', 'direction', 'average_speed']

        all_grouped.sort_values(by=['direction', 'zone'], inplace=True)

        # print(all_grouped)

        pre_dir = None
        for index, row in all_grouped.iterrows():
            if row['direction'] == pre_dir:
                obj = response['data'][f'direction-{int(row["direction"])}'][-1]
                new_one = False
            else:
                obj = {
                    "driverId": "all",
                    "speeds": []
                }
                new_one = True

            obj['speeds'].append({
                "zone": row['zone'],
                "average_speed": row['average_speed']
            })

            if new_one:
                response['data'][f'direction-{int(row["direction"])}'].append(obj)

            # assigning previous one
            pre_dir = row['direction']

        return response

    def get_speed_at_zones(self, start_date, end_date):

        if start_date or end_date:
            return self.__calculate_speed_at_zones(start_date, end_date)
        if self.__cache_valid:
            return self.__data
        else:
            self.__data = self.__calculate_speed_at_zones()
            self.__cache_valid = True
            return self.__data

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date
