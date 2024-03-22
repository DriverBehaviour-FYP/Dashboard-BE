from flask import Blueprint, jsonify, request
from app.main.controllers.summary.all_drivers_cache import AllDriverSummary
from app.main.controllers.summary.all_drivers_metadata_cache import AllDriverMetadata
from app.main.controllers.summary.all_drivers_dwell_time import AllDriverDwellTime
from app.main.controllers.summary.all_driver_speed_zones import AllDriverSpeed
from config.main_config import VERSION

summary_api_blueprint = Blueprint("api/summary", __name__)

global all_driver_summary
global all_driver_metadata
global all_driver_dwell_times
global all_driver_speed_at_zones

all_driver_summary = AllDriverSummary(version=VERSION)
all_driver_metadata = AllDriverMetadata(version=VERSION)
all_driver_dwell_times = AllDriverDwellTime(version=VERSION)
all_driver_speed_at_zones = AllDriverSpeed(version=VERSION)


@summary_api_blueprint.route('/api/alldrivers/summary/', methods=['POST'])
def get_summary():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    drivers = req_body.get('drivers')

    summary_data = all_driver_summary.get_summary(start_date, end_date, drivers)
    return jsonify({
        'success': True,
        'data':summary_data
    })


@summary_api_blueprint.route('/api/alldrivers/metadata/', methods=['POST'])
def get_summary_meta_data():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    drivers = req_body.get('drivers')
    metadata = all_driver_metadata.get_metadata(start_date, end_date, drivers)
    return jsonify({
        'success': True,
        'data':metadata
    })


@summary_api_blueprint.route('/api/alldrivers/dwelltime/', methods=['POST'])
def get_dwell_times():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    drivers = req_body.get('drivers')

    dwell_times = all_driver_dwell_times.get_dwell_times(start_date, end_date, drivers)
    return jsonify({
        'success': True,
        **dwell_times
    })


@summary_api_blueprint.route('/api/alldrivers/speedatzones/', methods=['POST'])
def get_speed_at_zones():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    drivers = req_body.get('drivers')

    speeds = all_driver_speed_at_zones.get_speed_at_zones(start_date, end_date, drivers)
    return jsonify({
        'success': True,
        **speeds
    })


@summary_api_blueprint.route('/api/alldrivers/ids/', methods=['POST'])
def get_all_driver_ids():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')

    drivers = all_driver_metadata.get_all_drivers(start_date, end_date)
    return jsonify({
        'success': True,
        'drivers': [int(x) for x in drivers]
    })