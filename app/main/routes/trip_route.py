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
    
@trip_api_blueprint.route('/api/trip/realtime/<segment_id>', methods=['GET'])
def get_trip_realtime(segment_id):
    segment_id = int(segment_id)
    print("DebugAssistant - 30")
    result = trip_controller.get_gps_data_with_cluster_realtime(segment_id)
    return  result
    # return result[0]
    # if gps_data['success']:
    #     return jsonify(gps_data)
    # else:
    #     return make_response(jsonify(gps_data), gps_data['statusCode'])