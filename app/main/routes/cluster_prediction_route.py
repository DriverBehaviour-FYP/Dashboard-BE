from datetime import datetime
from flask import Blueprint, jsonify, request
from app.main.loaders.model_loader import load
import json
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

clusterp_api_blueprint = Blueprint("api/cluster_prediction", __name__)

# Load the scaler, PCA, and model using pickle
model, scaler, pca = load(model_name='k-means', pca=True, no_pca_comp=3, no_classes=3, scaler=True)

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a)) 
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r*1000)

@clusterp_api_blueprint.route('/api/cluster/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is cluster prediction API'})


@clusterp_api_blueprint.route('/api/cluster/predict/', methods=['POST'])
def predict():
    data = json.loads(request.data).get('data')
    input_df = pd.DataFrame(data)
    ## asume:
        # 1) ### clean ######
        # 2) ### devide segment ########
        # 3) ### every point have elevation ########

    ####1) max_speed ######
    max_speed = max(input_df['speed'])
    ####2) speed_variation ######
    average_speed = np.mean(input_df[input_df['speed']>0]['speed'])
    
    speed_values = input_df['speed'].tolist()
    times = input_df['devicetime'].tolist()
    datetime_format = "%d/%m/%Y %H:%M"
    datetime_list = [datetime.strptime(time, datetime_format) for time in times]

    accelerations = []
    count_p =0
    count_n=0
    sum_elevation_p=0
    ac_sum_elevation_p=0
    sum_elevation_n=0
    ac_sum_elevation_n=0

    # Calculate accelerations
    for i in range(len(speed_values) - 1): 
        time_difference = (datetime_list[i + 1] - datetime_list[i]).total_seconds()
        elevation = input_df['elevation'][i+1]-input_df['elevation'][i]
        displacement = distance(input_df['latitude'][i+1],input_df['latitude'][i],input_df['longitude'][i+1],input_df['longitude'][i])
        
        # Check if the time difference is zero before division
        if time_difference != 0:
            acceleration = (speed_values[i + 1] - speed_values[i]) / time_difference
            accelerations.append(acceleration)
        if(elevation != 0 and displacement!=0):
          angle_tan = elevation/displacement
          if(angle_tan>0):
            sum_elevation_p+=angle_tan
            ac_sum_elevation_p+=angle_tan*(input_df['speed'][i+1]+input_df['speed'][i])/2
            count_p+=1
          elif(angle_tan<0):
            sum_elevation_n+=angle_tan
            ac_sum_elevation_n+=abs(angle_tan)*(input_df['speed'][i+1]+input_df['speed'][i])/2
            count_n+=1
    
    # Filter positive accelerations
    positive_accelerations = [acc for acc in accelerations if acc > 0]
    # Filter negative accelerations
    negative_accelerations = [acc for acc in accelerations if acc < 0]

    ####3) average_deacceleration ######
    average_deacceleration = sum(negative_accelerations) / len(negative_accelerations) if len(negative_accelerations) > 0 else np.nan
    ####4) average_acceleration ######
    average_acceleration = sum(positive_accelerations) / len(positive_accelerations) if len(positive_accelerations) > 0 else np.nan
    ####5) std_acc_dacc ######
    std_acc_dacc = np.std(accelerations) if len(accelerations) > 0 else np.nan
    ####6) elevation ######
    elevation_p = sum_elevation_p/count_p if count_p!=0 else 0
    elevation_n = sum_elevation_n/count_n if count_n!=0 else 0
    ele_X_speed_acc_p = ac_sum_elevation_p/count_p if count_p!=0 else 0
    ele_X_speed_acc_n =  ac_sum_elevation_n/count_n if count_n!=0 else 0
    
    ####7) stop count ######
    # Initialize variables
    stop_count = 0
    squared_diff_sum = 0
    is_stopped = False

    # Iterate through velocity values
    for velocity in speed_values:
        squared_diff_sum +=(velocity - average_speed) ** 2
        if velocity == 0 and not is_stopped:
            # Entered a stop, update stop count
            stop_count += 1
            is_stopped = True
        elif velocity != 0:
            # Left the stop, reset flag
            is_stopped = False
   
    ####8) speed_variation ######
    speed_variation = squared_diff_sum / len(speed_values)
    
    
    cluster_column = ['elevation_p', 'elevation_n', 'ele_X_speed_acc_p', 'ele_X_speed_acc_n',
                            'average_acceleration', 'average_deacceleration', 'std_acc_dacc',
                            'stop_count', 'average_speed', 'max_speed', 'speed_variation']

    new_dict = {'elevation_p':elevation_p, 'elevation_n':elevation_n, 'ele_X_speed_acc_p':ele_X_speed_acc_p, 'ele_X_speed_acc_n':ele_X_speed_acc_n,
                            'average_acceleration':average_acceleration, 'average_deacceleration':average_deacceleration, 'std_acc_dacc':std_acc_dacc,
                            'stop_count':stop_count, 'average_speed':average_speed, 'max_speed':max_speed, 'speed_variation':speed_variation}
    new_input_df = pd.DataFrame([new_dict])

    # Standardize numerical features only
    new_input_df[cluster_column] = scaler.transform(new_input_df[cluster_column])

    # Apply PCA
    pca_result = pca.transform(new_input_df[cluster_column])
    result = model.predict(pca_result)
    python_list = result.tolist()
    return jsonify({'predictions': python_list[0]})

##########################################################
# def predict():
#     data = json.loads(request.data).get('data')
#     input_df = pd.DataFrame([data])    
#     cluster_column = ['elevation_p', 'elevation_n', 'ele_X_speed_acc_p', 'ele_X_speed_acc_n',
#                             'average_acceleration', 'average_deacceleration', 'std_acc_dacc',
#                             'stop_count', 'average_speed', 'max_speed', 'speed_variation']

#     # Standardize numerical features only
#     input_df[cluster_column] = scaler.transform(input_df[cluster_column])

#     # Apply PCA
#     pca_result = pca.transform(input_df[cluster_column])
#     result = model.predict(pca_result)
#     python_list = result.tolist()
#     return jsonify({'predictions': python_list[0]})

#################################################################
# def predict():
#     data = json.loads(request.data).get('data')
#     print(type(data))
#     input_df = pd.DataFrame([data])

#     selected_features = ['segment_starting_time', 'segment_ending_time', 'trip_id', 'deviceid', 'date',
#                          'start_terminal',
#                          'end_terminal', 'direction', 'day_of_week', 'hour_of_day', 'segment_id', 'average_speed',
#                          'max_speed', 'speed_variation', 'elevation_p', 'elevation_n', 'ele_X_speed_acc_p',
#                          'ele_X_speed_acc_n', 'average_acceleration', 'average_deacceleration', 'std_acc_dacc',
#                          'stop_count']

#     temp_list = []
#     datetime_columns = ['segment_starting_time', 'segment_ending_time', 'date']
#     id_columns_list = ['trip_id', 'segment_id', 'deviceid']
#     catogorical_columns_list = ['start_terminal', 'end_terminal', 'direction']
#     temp_list.extend(datetime_columns)
#     temp_list.extend(id_columns_list)
#     temp_list.extend(catogorical_columns_list)
#     numerical_features = [col for col in selected_features if col not in temp_list]

#     # Standardize numerical features only
#     input_df[numerical_features] = scaler.transform(input_df[numerical_features])

#     cluster_column = []
#     cluster_column.extend(numerical_features)
#     cluster_column.extend(catogorical_columns_list)
#     elements_to_remove = ['start_terminal', 'end_terminal']
#     cluster_column_2 = [item for item in cluster_column if item not in elements_to_remove]

#     # Apply PCA
#     pca_result = pca.transform(input_df[cluster_column_2])

#     # Check if there's only one sample and duplicate it to meet the minimum requirement
#     if pca_result.shape[0] == 1:
#         pca_result = np.concatenate(
#             [pca_result, pca_result, pca_result, pca_result, pca_result, pca_result, pca_result, pca_result, pca_result,
#              pca_result])

#     result = model.fit_predict(pca_result)
#     print(result)
#     # return jsonify({'predictions': result})
#     return jsonify({'predictions': 'kk'})
