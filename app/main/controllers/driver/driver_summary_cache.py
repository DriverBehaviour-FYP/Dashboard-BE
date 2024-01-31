import pandas as pd
from app.main.loaders.data_loader import Data


class DriverSummary:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = dict()
        self.__metadata_valid = True

    def __calculate_driver_summary(self, driver_id):
        trip_data_temp = self.__trips_data[self.__trips_data['deviceid'] == driver_id]
        gps_data_temp = self.__gps_data[self.__gps_data['deviceid'] == driver_id]
        segments_temp = self.__segments_data[self.__segments_data['deviceid'] == driver_id]

        data = {
            "driver_id": driver_id,
            "speed": {
                "max": gps_data_temp['speed'].max(),
                "avg": gps_data_temp['speed'].mean(),
                "min": 0
            },
            "acceleration": {
                "max": segments_temp['max_acceleration'].max(),
                "avg": ((segments_temp['average_acceleration'] * (segments_temp['no_acc_points'] - 1)).sum() / ((segments_temp['no_acc_points'] - 1).sum())),
                "min": 0
            },
            "de-acceleration": {
                "max": segments_temp['max_deacceleration'].min() * -1,
                "avg": ((segments_temp['average_deacceleration'] * (segments_temp['no_deacc_points'] - 1)).sum() / ((segments_temp['no_deacc_points'] - 1).sum())) * -1,
                "min": 0
            },
            "trip-time": {
                "min": trip_data_temp['duration_in_mins'].min(),
                "avg": trip_data_temp['duration_in_mins'].mean(),
                "max": trip_data_temp['duration_in_mins'].max()
            }
        }
        self.__data[driver_id] = data

        return data

    def get_driver_summary(self, driver_id):
        summary = self.__data.get(driver_id)
        if summary is None:
            return self.__calculate_driver_summary(driver_id)
        else:
            return summary

