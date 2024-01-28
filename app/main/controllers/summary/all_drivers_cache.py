import pandas as pd
from app.main.loaders.data_loader import Data


class AllDriverSummary:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data(self.__version).get_gps_data()
        self.__segments_data = Data(self.__version).get_segments_data()
        self.__trips_data = Data(self.__version).get_trips_data()
        self.__data = self.__calculate_summary()
        self.__summary_valid = True

    def __calculate_summary(self):
        data = {
            'speed': {
                'max': self.__gps_data['speed'].max(),
                'avg': self.__gps_data['speed'].mean()
            },
            'acceleration': {
                'max': self.__segments_data['max_acceleration'].max(),
                'avg': ((self.__segments_data['average_acceleration'] * (self.__segments_data['no_data_points'] - 1)).sum()/ len(self.__segments_data)) * -1
            },
            'deacceleration': {
                'max':  self.__segments_data['max_deacceleration'].min() * -1,
                'avg': (self.__segments_data['average_deacceleration'] * (self.__segments_data['no_data_points'] - 1)).sum()/ len(self.__segments_data)
            },
            'trip-time': {
                "min": self.__trips_data['duration_in_mins'].min(),
                "avg": self.__trips_data['duration_in_mins'].mean(),
                "max": self.__trips_data['duration_in_mins'].max()
            }
        }
        return data

    def get_summary(self):
        if self.__summary_valid:
            return self.__data
        else:
            self.__data = self.__calculate_summary()
            self.__summary_valid = True
            return self.__data

