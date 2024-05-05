from flask import Blueprint, jsonify,make_response, request
from app.main.controllers.trip.trip_scores import TripScore
from app.main.controllers.trip.trip_controller import TripController
from config.main_config import VERSION

global trip_controller;
global trip_score;

trip_controller = TripController(version=VERSION)
trip_score = TripScore(version=VERSION)

trip_api_blueprint = Blueprint("api/trip", __name__)


@trip_api_blueprint.route('/api/trip/summary/<trip_id>', methods=['GET'])
def get_trip_summary(trip_id):
    trip_id = int(trip_id)
    summary = trip_controller.get_trip_summary(trip_id)
    if summary['success']:
        return jsonify(summary)
    else:
        return make_response(jsonify(summary), summary['statusCode'])


@trip_api_blueprint.route('/api/trip/metadata/<trip_id>', methods=['GET'])
def get_trip_metadata(trip_id):
    trip_id = int(trip_id)
    metadata = trip_controller.get_trip_metadata(trip_id)

    if metadata['success']:
        return jsonify(metadata)
    else:
        return make_response(jsonify(metadata), metadata['statusCode'])


@trip_api_blueprint.route('/api/trip/score/<device_id>', methods=['POST'])
def get_trip_score(device_id):
    device_id = int(device_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')

    trip_scores = trip_score.getScoresOfTrips(device_id, start_date, end_date)
    trip_scores['trip_id'] = [int(x) for x in trip_scores['trip_id']]
    return jsonify({
        "success": True,
        "data":trip_scores
    })


@trip_api_blueprint.route('/api/trip/gps/<trip_id>', methods=['GET'])
def get_trip_gps(trip_id):

    trip_id = int(trip_id)

    trip_behaviour = trip_controller.get_trip_behaviour(trip_id)

    return jsonify({
        "success": True,
        "data":trip_behaviour
    })


@trip_api_blueprint.route('/api/trip/dwelltime/<trip_id>', methods=['GET'])
def get_trip_dwell_times(trip_id):
    trip_id = int(trip_id)
    dwell_times = trip_controller.get_trip_dwell_times(trip_id)

    if dwell_times['success']:
        return jsonify(dwell_times)
    else:
        return make_response(jsonify(dwell_times), dwell_times['statusCode'])


@trip_api_blueprint.route('/api/trip/speedatzones/<trip_id>', methods=['GET'])
def get_trip_speed_at_zones(trip_id):
    trip_id = int(trip_id)
    speeds = trip_controller.get_speed_at_zones(trip_id)

    if speeds['success']:
        return jsonify(speeds)
    else:
        return make_response(jsonify(speeds), speeds['statusCode'])


@trip_api_blueprint.route('/api/trip/speedpercentages/<trip_id>', methods=['GET'])
def get_trip_speed_percentages(trip_id):
    trip_id = int(trip_id)
    speeds = trip_controller.get_speed_percentages(trip_id)

    if speeds['success']:
        return jsonify(speeds)
    else:
        return make_response(jsonify(speeds), speeds['statusCode'])

def get_first_occurrence_coordinates(data):
        first_occurrences = {}
        for item in data:
            segment_id = item.get('segment_id')
            if segment_id is not None:
                if segment_id not in first_occurrences:
                    first_occurrences[segment_id] = {'latitude': item['latitude'], 'longitude': item['longitude']}
        return list(first_occurrences.values())

def get_last_segment_coordinates(records):
    last_segment_coordinates = []
    last_segment_id = None
    first_record = records[0]
    first_latitude = first_record.get("latitude")
    first_longitude = first_record.get("longitude")
    last_segment_coordinates.append({"latitude": first_latitude, "longitude": first_longitude})
    
    for record in records:
        segment_id = record.get("segment_id")
        latitude = record.get("latitude")
        longitude = record.get("longitude")
        
        if segment_id != last_segment_id:
            last_segment_coordinates.append({"latitude": latitude, "longitude": longitude})
            last_segment_id = segment_id
    
    return last_segment_coordinates
   
@trip_api_blueprint.route('/api/trip/realtime/<segment_id>', methods=['GET'])
def get_trip_realtime(segment_id):
    segment_id = int(segment_id)
    print("DebugAssistant - 30")
    result, next_label = trip_controller.get_gps_data_with_cluster_realtime(segment_id)
    return  { "data": {
        "gps": result,
        "next_label": next_label.tolist()[0],
        "split_points": [
            {
                "latitude": 7.2989833,
                "longitude": 80.734055
            },
            {
                "latitude": 7.29584995,
                "longitude": 80.72992825
            },
            {
                "latitude": 7.2924208,
                "longitude": 80.72279495000001
            },
            {
                "latitude": 7.2854391,
                "longitude": 80.7223591
            },
            {
                "latitude": 7.285784100000001,
                "longitude": 80.71553665
            },
            {
                "latitude": 7.287355,
                "longitude": 80.70896995000001
            },
            {
                "latitude": 7.2839516500000006,
                "longitude": 80.7018483
            },
            {
                "latitude": 7.2814157999999995,
                "longitude": 80.6858641
            },
            {
                "latitude": 7.279225,
                "longitude": 80.6781033
            },
            {
                "latitude": 7.2810925,
                "longitude": 80.67004990000001
            },
            {
                "latitude": 7.285175000000001,
                "longitude": 80.66254415
            },
            {
                "latitude": 7.29021245,
                "longitude": 80.65579579999999
            },
            {
                "latitude": 7.2937224,
                "longitude": 80.64966495
            },
            {
                "latitude": 7.2908174500000005,
                "longitude": 80.64516165
            },
            {
                "latitude": 7.2875733,
                "longitude": 80.64600745
            },
            {
                "latitude": 7.2903633,
                "longitude": 80.6393933
            },
            {
                "latitude": 7.2916533,
                "longitude": 80.6352183
            }
        ]} ,  "success": True}
    # return result[0]
    # if gps_data['success']:
    #     return jsonify(gps_data)
    # else:
    #     return make_response(jsonify(gps_data), gps_data['statusCode'])