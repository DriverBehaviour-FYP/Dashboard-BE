from flask import Blueprint, jsonify
from app.main.controllers.trip.trip_scores import TripScore
from app.main.controllers.trip.trip_controller import TripController

global trip_controller;
global trip_score;

trip_controller = TripController()
trip_score = TripScore()

trip_api_blueprint = Blueprint("api/trip", __name__)


@trip_api_blueprint.route('/api/trip/<trip_id>', methods=['GET'])
def get_trip_summary(trip_id):
    trip_id = int(trip_id)
    summary = trip_controller.get_trip_summary(trip_id)
    return jsonify({
        "success": True,
        **summary
    })


@trip_api_blueprint.route('/api/trip/metadata/<trip_id>', methods=['GET'])
def get_trip_metadata(trip_id):
    trip_id = int(trip_id)
    metadata = trip_controller.get_trip_metadata(trip_id)
    return jsonify({
        "success": True,
        **metadata
    })

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
        "gps": trip_behaviour
    })
