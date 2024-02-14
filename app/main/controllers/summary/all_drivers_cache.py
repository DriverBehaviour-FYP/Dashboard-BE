import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE
import pandas as pd
from datetime import datetime as d


def refine_dates(start_date, end_date):
    start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime("2021-10-01")
    end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(d.now().strftime("%Y-%m-%d"))
    return start_date, end_date


class AllDriverSummary:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data(self.__version).get_gps_data()
        self.__segments_data = Data(self.__version).get_segments_data()
        self.__trips_data = Data(self.__version).get_trips_data()
        self.__data = self.__calculate_summary()
        self.__summary_valid = True

    def __calculate_summary(self, start=None, end=None):

        start_date, end_date = refine_dates(start, end)
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
            'cluster-summary': {
                "aggressive": len(segments_data[segments_data['cluster'] == AGGRESSIVE]),
                "normal": len(segments_data[segments_data['cluster'] == NORMAL]),
                "safe": len(segments_data[segments_data['cluster'] == SAFE]),
            }
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
