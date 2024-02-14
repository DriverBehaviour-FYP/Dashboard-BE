from flask import Blueprint, jsonify, request
from app.main.controllers.summary.all_drivers_cache import AllDriverSummary
from app.main.controllers.summary.all_drivers_metadata_cache import AllDriverMetadata
from config.main_config import VERSION

summary_api_blueprint = Blueprint("api/summary", __name__)

global all_driver_summary
global all_driver_metadata

all_driver_summary = AllDriverSummary(version=VERSION)
all_driver_metadata = AllDriverMetadata(version=VERSION)


@summary_api_blueprint.route('/api/alldrivers/summary/', methods=['POST'])
def get_summary():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')

    summary_data = all_driver_summary.get_summary(start_date, end_date)
    return jsonify({
        'success': True,
        **summary_data
    })


@summary_api_blueprint.route('/api/alldrivers/metadata/', methods=['POST'])
def get_summary_meta_data():
    req_body = request.get_json()

    start_date = req_body.get('start-date')
    end_date = req_body.get('end-date')
    metadata = all_driver_metadata.get_metadata(start_date, end_date)
    return jsonify({
        'success': True,
        **metadata
    })
