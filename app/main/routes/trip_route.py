from flask import Blueprint, jsonify
from app.main.controllers.trip.trip_controller import TripController

global trip_controller;

trip_controller = TripController()

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
