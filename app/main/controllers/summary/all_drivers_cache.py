import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE
import pandas as pd
from datetime import datetime as d


class AllDriverSummary:
    def __init__(self, version='1000M'):
        self.__version = version
        self.__gps_data = Data(self.__version).get_gps_data()
        self.__segments_data = Data(self.__version).get_segments_data()
        self.__trips_data = Data(self.__version).get_trips_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = self.__calculate_summary()
        self.__summary_valid = True

    def __calculate_summary(self, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)
        gps_data = self.__gps_data[(self.__gps_data['date'] >= start_date) & (self.__gps_data['date'] <= end_date)]
        trips_data = self.__trips_data[(self.__trips_data['date'] >= start_date) & (self.__trips_data['date'] <= end_date)]
        segments_data = self.__segments_data[(self.__segments_data['date'] >= start_date) & (self.__segments_data['date'] <= end_date)]

        data = {
            "success": True,
            'speed': {
                'max': gps_data['speed'].max(),
                'avg': gps_data['speed'].mean()
            },
            'acceleration': {
                'max': segments_data['average_acceleration'].max(),
                'avg': (segments_data['average_acceleration'] * (
                            segments_data['no_acc_points'] - 1)).sum() / (
                           (segments_data['no_acc_points'] - 1).sum())
            },
            'de-acceleration': {
                'max': segments_data['average_deacceleration'].min() * -1,
                'avg': ((segments_data['average_deacceleration'] * (
                            segments_data['no_deacc_points'] - 1)).sum() / (
                            (segments_data['no_deacc_points'] - 1).sum())) * -1
            },
            'trip-time': {
                "min": trips_data['duration_in_mins'].min(),
                "avg": trips_data['duration_in_mins'].mean(),
                "max": trips_data['duration_in_mins'].max()
            },
            'all-cluster-summary': {
                "aggressive": len(segments_data[segments_data['cluster'] == AGGRESSIVE]),
                "normal": len(segments_data[segments_data['cluster'] == NORMAL]),
                "safe": len(segments_data[segments_data['cluster'] == SAFE]),
            },
            "selected-start-date": start_date.strftime("%Y-%M-%d"),
            "selected-end-date": end_date.strftime("%Y-%M-%d"),
            "start-date": self.__metadata_f_file['data-collection-start-date'],
            "end-date": self.__metadata_f_file['data-collection-end-date']
        }
        return data

    def get_summary(self, start_date, end_date):

        if start_date or end_date:
            return self.__calculate_summary(start_date, end_date)
        if self.__summary_valid:
            return self.__data
        else:
            self.__data = self.__calculate_summary()
            self.__summary_valid = True
            return self.__data

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date
