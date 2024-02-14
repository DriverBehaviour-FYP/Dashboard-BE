import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE
from datetime import datetime as d


def refine_dates(start_date, end_date):
    start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime("2021-10-01")
    end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(d.now().strftime("%Y-%m-%d"))
    return start_date, end_date


class DriverSummary:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_driver_summary(self, driver_id, start=None, end=None):

        start_date, end_date = refine_dates(start, end)
        trip_data_temp = self.__trips_data[(self.__trips_data['deviceid'] == driver_id) & (self.__trips_data['date'] >= start_date) & (self.__trips_data['date'] <= end_date)]
        gps_data_temp = self.__gps_data[(self.__gps_data['deviceid'] == driver_id) & (self.__gps_data['date'] >= start_date) & (self.__gps_data['date'] <= end_date)]
        segments_temp = self.__segments_data[(self.__segments_data['deviceid'] == driver_id) & (self.__segments_data['date'] >= start_date) & (self.__segments_data['date'] <= end_date)]

        trip_data_temp.reset_index(inplace=True)
        gps_data_temp.reset_index(inplace=True)
        segments_temp.reset_index(inplace=True)

        if len(trip_data_temp) == 0 or len(gps_data_temp) == 0 or len(segments_temp) == 0:
            if start or end:
                return {"success": False, "errorMessage": "No data for requested date range!", "statusCode": 400}
            return {"success": False, "errorMessage": "Driver not found!", "statusCode": 400}

        data = {
            "success": True,
            "driver_id": driver_id,
            "selected-start-date": start_date.strftime("%Y-%m-%d"),
            "selected-end-date": end_date.strftime("%Y-%m-%d"),
            "speed": {
                "max": gps_data_temp['speed'].max(),
                "avg": gps_data_temp['speed'].mean(),
                "min": 0
            },
            "acceleration": {
                "max": segments_temp['average_acceleration'].max(),
                "avg": ((segments_temp['average_acceleration'] * (segments_temp['no_acc_points'] - 1)).sum() / ((segments_temp['no_acc_points'] - 1).sum())),
                "min": 0
            },
            "de-acceleration": {
                "max": segments_temp['average_deacceleration'].min() * -1,
                "avg": ((segments_temp['average_deacceleration'] * (segments_temp['no_deacc_points'] - 1)).sum() / ((segments_temp['no_deacc_points'] - 1).sum())) * -1,
                "min": 0
            },
            "trip-time": {
                "min": trip_data_temp['duration_in_mins'].min(),
                "avg": trip_data_temp['duration_in_mins'].mean(),
                "max": trip_data_temp['duration_in_mins'].max()
            },
            "cluster-summary": {
                "aggressive": len(segments_temp[segments_temp['cluster'] == AGGRESSIVE]),
                "normal": len(segments_temp[segments_temp['cluster'] == NORMAL]),
                "safe": len(segments_temp[segments_temp['cluster'] == SAFE]),
            }
        }
        return data

    def get_driver_summary(self, driver_id, start_date, end_date):
        return self.__calculate_driver_summary(driver_id, start_date, end_date)


