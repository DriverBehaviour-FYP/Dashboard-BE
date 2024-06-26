from flask import Blueprint, jsonify, make_response, request
import numpy as np
from app.main.controllers.driver.driver_metadata_cache import DriverMetadata
from app.main.controllers.driver.driver_summary_cache import DriverSummary
from app.main.controllers.driver.driver_dwell_times import DriverDwellTimes
from app.main.controllers.driver.speed_controller import DriverSpeedController
from app.main.controllers.driver.driver_scores import DriverScore
from config.main_config import VERSION

driver_api_blueprint = Blueprint("api/driver", __name__)

global driver_metadata
global driver_summary
global driver_score
global driver_dwell_times
global driver_speed

driver_metadata = DriverMetadata(version=VERSION)
driver_summary = DriverSummary(version=VERSION)
driver_score = DriverScore(version=VERSION)
driver_dwell_times = DriverDwellTimes(version=VERSION)
driver_speed = DriverSpeedController(version=VERSION)


@driver_api_blueprint.route('/api/driver/summary/<driver_id>', methods=['POST'])
def get_driver_summary(driver_id):
    driver_id = int(driver_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    trips = req_body.get('trips')

    summary = driver_summary.get_driver_summary(driver_id, start_date, end_date, trips)

    if summary['success']:
        return jsonify(summary)
    else:
        return make_response(summary, summary['statusCode'])


@driver_api_blueprint.route('/api/driver/metadata/<driver_id>', methods=['POST'])
def get_summary_meta_data(driver_id):
    driver_id = int(driver_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    trips = req_body.get('trips')

    metadata = driver_metadata.get_driver_metadata(driver_id, start_date, end_date, trips)
    if metadata['success']:
        return jsonify(metadata)
    else:
        return make_response(metadata, metadata['statusCode'])


@driver_api_blueprint.route('/api/driver/score', methods=['POST'])
def get_driver_scores():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    drivers = req_body.get('drivers')

    scores = driver_score.getScoresOfDrivers(start_date, end_date, drivers)

    return jsonify({'success': True,
                    'data': scores})


@driver_api_blueprint.route('/api/driver/dwelltime/<driver_id>', methods=['POST'])
def get_driver_dwell_times(driver_id):
    driver_id = int(driver_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    trips = req_body.get('trips')

    dwell_times = driver_dwell_times.get_driver_dwell_times(driver_id, start_date, end_date, trips)

    if dwell_times['success']:
        return jsonify(dwell_times)
    else:
        return make_response(dwell_times, dwell_times['statusCode'])


@driver_api_blueprint.route('/api/driver/speedpercentages/<driver_id>', methods=['POST'])
def get_driver_speed_percentages(driver_id):
    driver_id = int(driver_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    trips = req_body.get('trips')

    speed_percentages = driver_speed.get_speed_percentages(driver_id, start_date, end_date, trips)

    if speed_percentages['success']:
        return jsonify(speed_percentages)
    else:
        return make_response(speed_percentages, speed_percentages['statusCode'])


@driver_api_blueprint.route('/api/driver/tripids/<driver_id>', methods=['POST'])
def get_driver_trip_ids(driver_id):
    driver_id = int(driver_id)
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')

    res = driver_metadata.get_trip_ids(driver_id, start_date, end_date)

    if res['success']:
        return jsonify(res)
    else:
        return make_response(res, res['statusCode'])
