import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE


class DriverSummary:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_summary(self, driver_id, start_date, end_date, direction=None, trips=None):
        trip_data_temp = self.__trips_data[
            (self.__trips_data['deviceid'] == driver_id) & (self.__trips_data['date'] >= start_date) & (
                        self.__trips_data['date'] <= end_date)]
        gps_data_temp = self.__gps_data[
            (self.__gps_data['deviceid'] == driver_id) & (self.__gps_data['date'] >= start_date) & (
                        self.__gps_data['date'] <= end_date)]
        segments_temp = self.__segments_data[
            (self.__segments_data['deviceid'] == driver_id) & (self.__segments_data['date'] >= start_date) & (
                        self.__segments_data['date'] <= end_date)]

        if direction:
            trip_data_temp = trip_data_temp[trip_data_temp['direction'] == direction]
            segments_temp = segments_temp[segments_temp['direction'] == direction]
            gps_data_temp = gps_data_temp[gps_data_temp['direction'] == direction]

        if (trips is not None) and len(trips) != 0:
            trip_data_temp = trip_data_temp[trip_data_temp['trip_id'].isin(trips)]
            segments_temp = segments_temp[segments_temp['trip_id'].isin(trips)]
            gps_data_temp = gps_data_temp[gps_data_temp['trip_id'].isin(trips)]

        trip_data_temp.reset_index(inplace=True)
        gps_data_temp.reset_index(inplace=True)
        segments_temp.reset_index(inplace=True)

        if len(trip_data_temp) == 0 or len(gps_data_temp) == 0 or len(segments_temp) == 0:
            return {
                "data-present": False
            }

        data = {
            "data-present": True,
            "speed": {
                "max": gps_data_temp['speed'].max(),
                "avg": gps_data_temp['speed'].mean(),
                "min": 0
            },
            "acceleration": {
                "max": segments_temp['average_acceleration'].max(),
                "avg": ((segments_temp['average_acceleration'] * (segments_temp['no_acc_points'] - 1)).sum() / (
                    (segments_temp['no_acc_points'] - 1).sum())),
                "min": 0
            },
            "de-acceleration": {
                "max": segments_temp['average_deacceleration'].min() * -1,
                "avg": ((segments_temp['average_deacceleration'] * (segments_temp['no_deacc_points'] - 1)).sum() / (
                    (segments_temp['no_deacc_points'] - 1).sum())) * -1,
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

    def get_driver_summary(self, driver_id, start=None, end=None, trips=None):

        # check whether driver id exists
        if not (driver_id in self.__trips_data['deviceid'].unique()):
            return {"success": False, "errorMessage": "Driver not found!", "statusCode": 400}

        start_date, end_date = self.refine_dates(start, end)

        data = {
            "success": True,
            "driver_id": driver_id,
            "selected-start-date": start_date.strftime("%Y-%m-%d"),
            "selected-end-date": end_date.strftime("%Y-%m-%d"),
            "direction-all": self.__calculate_summary(driver_id, start_date, end_date, direction=None, trips=trips),
            "direction-1": self.__calculate_summary(driver_id, start_date, end_date, direction=1, trips=trips),
            "direction-2": self.__calculate_summary(driver_id, start_date, end_date, direction=2, trips=trips),
            "start-date": self.__metadata_f_file['data-collection-start-date'],
            "end-date": self.__metadata_f_file['data-collection-end-date']
        }
        return { "success": True,"data" :data}

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date


