import pandas as pd
from app.main.loaders.json_loader import load_json_path


def load_and_convert(path):
    data = pd.read_csv(path)
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
    return data



class Data:
    _instance = None  # Class variable to store the single instance

    def __new__(cls, version='1000M'):

        # Create a new instance only if it doesn't exist
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__gps_data = load_and_convert(f"./data/preprocessed/{version}/merged_gps_data_{version}.csv")
            cls._instance.__segments_data = load_and_convert(f"./data/preprocessed/{version}/merged_segments_data_{version}.csv")
            cls._instance.__trips_data = load_and_convert(f"./data/preprocessed/common/merged_trips_data.csv")
            cls._instance.__bus_stops = load_and_convert("./data/preprocessed/common/bus_stops_654.csv")
            cls._instance.__cluster_data = load_and_convert(f"./data/preprocessed/{version}/merged_cluster_data_{version}.csv")
            cls._instance.__bus_terminals = load_and_convert("./data/preprocessed/common/bus_terminals_654.csv")
            cls._instance.__metadata = load_json_path(f'./data/preprocessed/{version}/meta_data_{version}.json')
            cls._instance.__dwellTimes = load_and_convert("./data/preprocessed/common/all_dwell_times.csv")
            cls._instance.__speed_at_zones = load_and_convert("./data/preprocessed/common/zone_wise_speed.csv")
            cls._instance.__common_metadata = load_json_path(f'./data/preprocessed/common/common_metadata.json')
            cls._instance.__gps_data_trip_1951 = load_and_convert(f'./data/preprocessed/trip_1951-gps.csv')
            cls._instance.__section_data_trip_1951 = load_and_convert(f'./data/preprocessed/trip_1951-segments.csv')
            cls._instance.__norms_df = load_and_convert(f'./data/preprocessed/norms_df.csv')

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

    def get_dwell_times(self):
        return self.__dwellTimes

    def get_speed_at_zones(self):
        return self.__speed_at_zones

    def get_common_metadata(self):
        return self.__common_metadata
    
    def get_gps_data_trip_1951(self):
        return self.__gps_data_trip_1951
    
    def get_section_data_trip_1951(self):
        return self.__section_data_trip_1951
    
    def get_norms_df(self):
        return self.__norms_df
