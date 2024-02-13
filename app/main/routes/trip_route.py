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


@trip_api_blueprint.route('/api/trip/score/<device_id>', methods=['GET'])
def get_trip_score(device_id):
    device_id = int(device_id)
    trip_scores = trip_score.getScoresOfTrips(device_id)
    trip_scores['trip_id'] = [int(x) for x in trip_scores['trip_id']]
    return jsonify({
        "success": True,
        **trip_scores
    })


@trip_api_blueprint.route('/api/trip/gps/<trip_id>', methods=['GET'])
def get_trip_gps(trip_id):
    trip_id = int(trip_id)
    trip_behaviour = trip_controller.get_trip_behaviour(trip_id)
    return jsonify({
        "success": True,
        **trip_behaviour
    })
