import pandas as pd
from app.main.loaders.data_loader import Data



class DriverMetadata:
    def __init__(self, version='1000M'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__metadata_valid = True

    def __calculate_driver_metadata(self, driver_id, start_date, end_date, direction=None):
        temp_df = self.__trips_data[
            (self.__trips_data['deviceid'] == driver_id) & (self.__trips_data['date'] >= start_date) & (
                        self.__trips_data['date'] <= end_date)]

        if direction:
            temp_df = temp_df[temp_df['direction'] == direction]

        temp_df.reset_index(inplace=True)
        if len(temp_df) == 0:
            return {
                "data-present": False
            }

        data = {
            "no-of-trips": len(temp_df)
        }

        return data

    def get_driver_metadata(self, driver_id, start=None, end=None):
        start_date, end_date = self.refine_dates(start, end)

        # check whether driver id exists
        if not (driver_id in self.__trips_data['deviceid'].unique()):
            return {"success": False, "errorMessage": "Driver not found!", "statusCode": 400}

        data = {
            
            "driver-id": driver_id,
            "direction-all": self.__calculate_driver_metadata(driver_id,start_date, end_date, direction=None),
            "direction-1": self.__calculate_driver_metadata(driver_id, start_date, end_date, direction=1),
            "direction-2": self.__calculate_driver_metadata(driver_id, start_date, end_date, direction=2),
            "routes": self.__metadata_f_file['routes'],
            "data-collection-start-date": self.__metadata_f_file['data-collection-start-date'],
            "data-collection-end-date": self.__metadata_f_file['data-collection-end-date'],
            "data-collection-period": (pd.to_datetime(self.__metadata_f_file['data-collection-end-date']) - pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])).days,
            "selected-start-date": start_date.strftime("%Y-%m-%d"),
            "selected-end-date": end_date.strftime("%Y-%m-%d")
        }

        return {"success": True,"data":data}

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date

