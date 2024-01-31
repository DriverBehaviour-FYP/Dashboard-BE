import pandas as pd
from app.main.loaders.data_loader import Data


class TripController:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()

    def get_trip_metadata(self, trip_id):
        trip = self.__trips_data[self.__trips_data['trip_id'] == trip_id][0]
        segments = self.__segments_data[self.__segments_data['trip_id'] == trip_id]

        data = {
            "trip_id": trip_id,
            "duration": trip['duration'],
            "date": trip['date'],
            "start-time": trip['start_time'],
            "end-time": trip['end_time'],
            "no-segments": len(segments),
            "routes": self.__metadata_f_file['routes'],
        }
        return data

    def get_trip_summary(self, trip_id):
        segments = self.__segments_data[self.__segments_data['trip_id'] == trip_id]

        data = {
            "speed": {
                "min": 0,
                "avg": (segments['speed_mean'] * segments['no_data_points']).sum() / (segments['no_data_points'].sum()),
                "max": segments['speed_max'].max()
            },
            "acceleration": {
                "min": 0,
                "avg": ((segments['average_acceleration'] * (segments['no_data_points'] - 1)).sum() / ((segments['no_data_points'] - 1).sum())),
                "max": segments['max_acceleration'].max(),
            },
            "de-acceleration": {
                "min": 0,
                "avg": ((segments['average_deacceleration'] * (segments['no_data_points'] - 1)).sum() / ((segments['no_data_points'] - 1).sum())) * -1,
                "max": segments['max_deacceleration'].min() * -1,
            }
        }
        return data
