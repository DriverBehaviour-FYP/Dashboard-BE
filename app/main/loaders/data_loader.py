import pandas as pd
from app.main.loaders.json_loader import load_json_path


class Data:
    _instance = None  # Class variable to store the single instance

    def __new__(cls, version='10T'):
        # Create a new instance only if it doesn't exist
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__gps_data = pd.read_csv(f"./data/preprocessed/{version}/merged_gps_data_10T.csv")
            cls._instance.__segments_data = pd.read_csv(f"./data/preprocessed/{version}/merged_segments_data_10T.csv")
            cls._instance.__trips_data = pd.read_csv(f"./data/preprocessed/{version}/merged_trips_data.csv")
            cls._instance.__bus_stops = pd.read_csv("./data/preprocessed/common/bus_stops_654.csv")
            cls._instance.__cluster_data = pd.read_csv(f"./data/preprocessed/{version}/norms-clustering-results-original-f.csv")
            cls._instance.__bus_terminals = pd.read_csv("./data/preprocessed/common/bus_terminals_654.csv")
            cls._instance.__metadata = load_json_path(f'./data/preprocessed/{version}/meta_data.json')
        return cls._instance

    def get_gps_data(self):
        return self.__gps_data

    def get_segments_data(self):
        return self.__segments_data

    def get_trips_data(self):
        return self.__trips_data

    def get_bus_stops_data(self):
        return self.__bus_stops

    def get_bus_terminals_data(self):
        return self.__bus_terminals

    def get_metadata(self):
        return self.__metadata
    
    def get_clusterdata(self):
        return self.__cluster_data
