import pandas as pd
from app.main.loaders.data_loader import Data
import json


class DriverScore:
    def __init__(self, version='10T'):
        self.__version = version
        self.__gps_data = Data().get_gps_data()
        self.__segments_data = Data().get_segments_data()
        self.__trips_data = Data().get_trips_data()
        self.__bus_stops = Data().get_bus_stops_data()
        self.__clusterdata = Data().get_clusterdata()
        self.__metadata_f_file = Data().get_metadata()
        self.__data = dict()
        self.__metadata_valid = True

    def ScoreDriver(self, deviceid, cluster_data):
        filtered_df = cluster_data[cluster_data['deviceid'] == deviceid]
        cluster_counts = filtered_df['cluster'].value_counts().reset_index()
        cluster_counts.columns = ['cluster', 'count']
        cluster_scores = {0: 100, 1: 80, 2: 10}
        weighted_score = (cluster_counts.apply(lambda row: cluster_scores.get(row['cluster'], 0) * row['count'],
                                               axis=1).sum() / sum(cluster_counts['count']))
        return weighted_score.round(2)
        # print(f"Device Score: {weighted_score:.2f} out of 100")

    def getScoresOfDrivers(self, start=None, end=None):

        start_date, end_date = self.refine_dates(start, end)

        cluster_data = self.__clusterdata[(self.__clusterdata['date'] >= start_date) & (self.__clusterdata['date'] <= end_date)]

        unique_device_ids = cluster_data['deviceid'].unique()

        output = {
            'deviceid': [],
            'score': [],
            'scaledScores': []
        }

        for deviceId in unique_device_ids:
            score = self.ScoreDriver(deviceId, cluster_data)
            output['deviceid'].append(deviceId)
            output['score'].append(score)

        min_val = min(output['score'])
        max_val = max(output['score'])

        scaledScore = [((x - min_val) / (max_val - min_val) * 100).round(2) for x in output['score']]

        output['scaledScores'] = scaledScore
        output['start-date'] = start_date.strftime("%Y-%m-%d")
        output['end-date'] = end_date.strftime("%Y-%m-%d")
        # print(output)
        return output

    def refine_dates(self, start_date, end_date):
        start_date = pd.to_datetime(start_date) if start_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-start-date'])
        end_date = pd.to_datetime(end_date) if end_date else pd.to_datetime(
            self.__metadata_f_file['data-collection-end-date'])
        return start_date, end_date
