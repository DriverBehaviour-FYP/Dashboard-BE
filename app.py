from flask import Flask , request , jsonify , render_template
import json
import pickle
import numpy as np
import pandas as pd

# Load the scaler, PCA, and model using pickle
with open('Model/spectral/spectral_pca-3_class-3.pkl','rb') as file:
    model = pickle.load(file)
with open('Model/spectral/spectral_pca-3_class-3_scaler.pkl','rb') as file:
    scaler = pickle.load(file)
with open('Model/spectral/spectral_pca-3_class-3_PCA.pkl','rb') as file:
    pca = pickle.load(file)

app = Flask(__name__)


@app.route('/')
def Home():
    return 'Hello, Flask!'

@app.route('/predict',methods = ['POST'])
def predict():
    data = json.loads(request.data).get('data')
    print(type(data))
    input_df = pd.DataFrame([data])
    
    selected_features = ['segment_starting_time', 'segment_ending_time', 'trip_id', 'deviceid', 'date', 'start_terminal',
                      'end_terminal', 'direction', 'day_of_week', 'hour_of_day', 'segment_id', 'average_speed',
                      'max_speed', 'speed_variation', 'elevation_p', 'elevation_n', 'ele_X_speed_acc_p',
                      'ele_X_speed_acc_n', 'average_acceleration', 'average_deacceleration', 'std_acc_dacc',
                      'stop_count']
    
    temp_list = []
    datetime_columns = ['segment_starting_time', 'segment_ending_time', 'date']
    id_columns_list = ['trip_id', 'segment_id','deviceid']
    catogorical_columns_list = ['start_terminal','end_terminal','direction']
    temp_list.extend(datetime_columns)
    temp_list.extend(id_columns_list)
    temp_list.extend(catogorical_columns_list)
    numerical_features = [col for col in selected_features if col not in temp_list]

    # Standardize numerical features only
    input_df[numerical_features] = scaler.transform(input_df[numerical_features])

    cluster_column = []
    cluster_column.extend(numerical_features)
    cluster_column.extend(catogorical_columns_list)
    elements_to_remove = ['start_terminal','end_terminal']
    cluster_column_2 = [item for item in cluster_column if item not in elements_to_remove]

    # Apply PCA
    pca_result = pca.transform(input_df[cluster_column_2])

    # Check if there's only one sample and duplicate it to meet the minimum requirement
    if pca_result.shape[0] == 1:
        pca_result = np.concatenate([pca_result, pca_result,pca_result, pca_result,pca_result, pca_result,pca_result, pca_result,pca_result, pca_result])

    result = model.fit_predict(pca_result)
    print(result)
    # return jsonify({'predictions': result})
    return jsonify({'predictions': 'kk'})

if __name__ == '__main__':
    app.run(debug=True)
