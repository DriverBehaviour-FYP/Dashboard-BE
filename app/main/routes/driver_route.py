from flask import Blueprint, jsonify
import numpy as np
from app.main.controllers.driver.driver_metadata_cache import DriverMetadata
from app.main.controllers.driver.driver_summary_cache import DriverSummary
from app.main.controllers.driver.driver_scores import DriverScore

driver_api_blueprint = Blueprint("api/driver", __name__)

global driver_metadata;
global driver_summary;
global driver_score;

driver_metadata = DriverMetadata(version='10T')
driver_summary = DriverSummary(version='10T')
driver_score = DriverScore(version='10T')


@driver_api_blueprint.route('/api/driver/summary/<driver_id>', methods=['GET'])
def get_driver_summary(driver_id):
    driver_id = int(driver_id)
    summary = driver_summary.get_driver_summary(driver_id)
    return jsonify({
        "success": True,
        **summary
    })


@driver_api_blueprint.route('/api/driver/metadata/<driver_id>', methods=['GET'])
def get_summary_meta_data(driver_id):
    driver_id = int(driver_id)
    metadata = driver_metadata.get_driver_metadata(driver_id=driver_id)
    return jsonify({
        'success': True,
        **metadata
    })

@driver_api_blueprint.route('/api/driver/score', methods=['GET'])
def get_driver_scores():
    scores = driver_score.getScoresOfDrivers()
    scores['deviceid'] = [int(x) for x in scores['deviceid']]
    print(scores)
    return jsonify(scores)
