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
        self.__data = dict()
        self.__metadata_valid = True

    def ScoreDriver(self,deviceid):
        filtered_df = self.__clusterdata[self.__clusterdata['deviceid'] == deviceid]
        cluster_counts = filtered_df['cluster'].value_counts().reset_index()
        cluster_counts.columns = ['cluster', 'count']
        cluster_scores = {0: 100, 1: 80, 2: 20, 3: 10}
        weighted_score = (cluster_counts.apply(lambda row: cluster_scores.get(row['cluster'], 0) * row['count'], axis=1).sum() / sum(cluster_counts['count']))
        return weighted_score.round(2)
        # print(f"Device Score: {weighted_score:.2f} out of 100")

    def getScoresOfDrivers(self):
        unique_device_ids = self.__clusterdata['deviceid'].unique()

        output = {
            'deviceid' : [],
            'score' : [],
            'scaledScores' : []
        }

        for deviceId in unique_device_ids:
            score = self.ScoreDriver(deviceId)
            output['deviceid'].append(deviceId)
            output['score'].append(score)

        min_val = min(output['score'])
        max_val = max(output['score'])

        scaledScore = [((x - min_val) / (max_val - min_val) * 100).round(2) for x in output['score']]

        output['scaledScores'] = scaledScore
        # print(output)
        return output 