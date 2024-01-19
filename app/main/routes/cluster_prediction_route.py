from flask import Blueprint, jsonify, request
from app.main.loaders.model_loader import load
import json
import pandas as pd
import numpy as np

clusterp_api_blueprint = Blueprint("api/cluster_prediction", __name__)

# Load the scaler, PCA, and model using pickle
model, scaler, pca = load(model_name='k-means', pca=True, no_pca_comp=3, no_classes=3, scaler=True)


@clusterp_api_blueprint.route('/api/cluster/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is cluster prediction API'})


@clusterp_api_blueprint.route('/api/cluster/predict/', methods=['POST'])
def predict():
    data = json.loads(request.data).get('data')
    input_df = pd.DataFrame([data])    
    cluster_column = ['elevation_p', 'elevation_n', 'ele_X_speed_acc_p', 'ele_X_speed_acc_n',
                            'average_acceleration', 'average_deacceleration', 'std_acc_dacc',
                            'stop_count', 'average_speed', 'max_speed', 'speed_variation']

    # Standardize numerical features only
    input_df[cluster_column] = scaler.transform(input_df[cluster_column])

    # Apply PCA
    pca_result = pca.transform(input_df[cluster_column])
    result = model.predict(pca_result)
    python_list = result.tolist()
    return jsonify({'predictions': python_list[0]})

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
