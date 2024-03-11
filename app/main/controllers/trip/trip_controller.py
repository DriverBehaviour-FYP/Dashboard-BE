import pandas as pd
from app.main.loaders.data_loader import Data
from config.main_config import AGGRESSIVE, NORMAL, SAFE


class TripController:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__metadata_f_file = Data().get_metadata()
        self.__clusterdata = Data().get_clusterdata()
        self.__dwell_times = Data().get_dwell_times()
        self.__speed_at_zones = Data().get_speed_at_zones()
        self.__common_metadata = Data().get_common_metadata()

    def get_trip_metadata(self, trip_id):
        trips = self.__trips_data[self.__trips_data['trip_id'] == trip_id]
        trips.reset_index(inplace=True)
        if len(trips) == 0:
            print("vent to failing route")
            return {"success": False, "errorMessage": "Trip not found", "statusCode": 400}

        trip = trips.loc[0, :]
        segments = self.__segments_data[self.__segments_data['trip_id'] == trip_id]

        data = {
            "success": True,
            "trip-id": trip_id,
            "duration": trip['duration'],
            "date": trip['date'].strftime("%Y-%m-%d"),
            "start-time": trip['start_time'],
            "end-time": trip['end_time'],
            "no-segments": len(segments),
            "routes": self.__metadata_f_file['routes'],
        }
        return data

    def get_trip_summary(self, trip_id):
        segments = self.__segments_data[self.__segments_data['trip_id'] == trip_id]

        segments.reset_index(inplace=True)
        if len(segments) == 0:
            return {"success": False, "errorMessage": "Trip not found!", "statusCode": 400}

        data = {
            "success": True,
            "speed": {
                "min": 0,
                "avg": (segments['speed_mean'] * segments['no_data_points']).sum() / (segments['no_data_points'].sum()),
                "max": segments['speed_max'].max()
            },
            "acceleration": {
                "min": 0,
                "avg": ((segments['average_acceleration'] * (segments['no_acc_points'] - 1)).sum() / (
                    (segments['no_acc_points'] - 1).sum())),
                "max": segments['average_acceleration'].max(),
            },
            "de-acceleration": {
                "min": 0,
                "avg": ((segments['average_deacceleration'] * (segments['no_deacc_points'] - 1)).sum() / (
                    (segments['no_deacc_points'] - 1).sum())) * -1,
                "max": segments['average_deacceleration'].min() * -1,
            },
            "cluster-summary": {
                "aggressive": len(segments[segments['cluster'] == AGGRESSIVE]),
                "normal": len(segments[segments['cluster'] == NORMAL]),
                "safe": len(segments[segments['cluster'] == SAFE]),
            }
        }
        return data

    def __calculate_split_points(self, gps_data):

        gps_data.reset_index(inplace=True)

        split_points = []
        previous_row = None
        for index, row in gps_data.iterrows():
            if index == 0 or index == len(gps_data) - 1:
                split_points.append({"longitude": row['longitude'], 'latitude': row['latitude']})
            if (previous_row is not None) and row['segment_id'] != previous_row['segment_id']:
                split_points.append(
                    {
                        "longitude": (row['longitude'] + previous_row['longitude']) / 2,
                        "latitude": (row['latitude'] + previous_row['latitude']) / 2,
                    })
            previous_row = row
            df = pd.DataFrame(split_points)
        return df.to_dict(orient='records')

    def get_trip_behaviour(self, trip_id):
        cluster_data = self.__clusterdata[(self.__clusterdata['trip_id'] == trip_id)].reset_index()
        gps_data = self.__gps_data[(self.__gps_data['trip_id'] == trip_id)].reset_index()
        merged_df = pd.merge(gps_data, cluster_data[['segment_id', 'cluster']], on='segment_id', how='left')
        # merged_df['cluster'] = merged_df.groupby('segment_id')['cluster'].ffill()
        gps_data['cluster'] = merged_df['cluster']

        response = {
            "gps": gps_data.to_dict(orient='records'),
            "split_points": self.__calculate_split_points(gps_data),
        }
        return response

    def get_trip_dwell_times(self, trip_id):
        dwell_times = self.__dwell_times[self.__dwell_times['trip_id'] == trip_id]

        grouped_df = dwell_times.groupby(['bus_stop']).agg(
            average_dwell_time=('dwell_time_in_seconds', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['bus_stop_no', 'average_dwell_time']

        return {
            "data": grouped_df.to_dict(orient='records'),
            "success": True
        }

    def get_speed_at_zones(self, trip_id):
        speed_at_zones = self.__speed_at_zones[self.__speed_at_zones['trip_id'] == trip_id]

        speed_at_zones = speed_at_zones[speed_at_zones['zone'] % 1 != 0]

        grouped_df = speed_at_zones.groupby(['zone']).agg(
            average_dwell_time=('speed', 'mean')
        ).reset_index()

        # Renaming columns for clarity if necessary
        grouped_df.columns = ['zone', 'average_speed']

        return {
            "data": grouped_df.to_dict(orient='records'),
            "success": True
        }

    def get_speed_percentages(self, trip_id):
        gps_data = self.__gps_data[self.__gps_data['trip_id'] == trip_id]

        gps_data = gps_data[gps_data['speed'] != 0]

        response = {
            "success": True,
            "total-length": len(gps_data),
            'higher-than-3rd-quantile': len(gps_data[gps_data['speed'] >= self.__common_metadata['3rd-quantile']]),
            'lower-than-1st-quantile': len(gps_data[gps_data['speed'] <= self.__common_metadata['1st-quantile']]),
        }
        response['between'] = response['total-length'] - response['higher-than-3rd-quantile'] - response[
            'lower-than-1st-quantile']

        return response
