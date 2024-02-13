from flask import Blueprint, jsonify, make_response
import numpy as np
from app.main.controllers.driver.driver_metadata_cache import DriverMetadata
from app.main.controllers.driver.driver_summary_cache import DriverSummary
from app.main.controllers.driver.driver_scores import DriverScore
from config.main_config import VERSION

driver_api_blueprint = Blueprint("api/driver", __name__)

global driver_metadata;
global driver_summary;
global driver_score;

driver_metadata = DriverMetadata(version=VERSION)
driver_summary = DriverSummary(version=VERSION)
driver_score = DriverScore(version=VERSION)


@driver_api_blueprint.route('/api/driver/summary/<driver_id>', methods=['GET'])
def get_driver_summary(driver_id):
    driver_id = int(driver_id)
    summary = driver_summary.get_driver_summary(driver_id)

    if summary['success']:
        return jsonify(summary)
    else:
        return make_response(summary, summary['statusCode'])


@driver_api_blueprint.route('/api/driver/metadata/<driver_id>', methods=['GET'])
def get_summary_meta_data(driver_id):
    driver_id = int(driver_id)
    metadata = driver_metadata.get_driver_metadata(driver_id=driver_id)
    if metadata['success']:
        return jsonify(metadata)
    else:
        return make_response(metadata, metadata['statusCode'])

@driver_api_blueprint.route('/api/driver/score', methods=['GET'])
def get_driver_scores():
    scores = driver_score.getScoresOfDrivers()
    scores['deviceid'] = [int(x) for x in scores['deviceid']]
    print(scores)
    return jsonify(scores)
