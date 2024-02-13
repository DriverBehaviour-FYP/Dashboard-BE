from flask import Blueprint, jsonify
from app.main.controllers.summary.all_drivers_cache import AllDriverSummary
from app.main.controllers.summary.all_drivers_metadata_cache import AllDriverMetadata
from config.main_config import VERSION

summary_api_blueprint = Blueprint("api/summary", __name__)

global all_driver_summary
global all_driver_metadata

all_driver_summary = AllDriverSummary(version=VERSION)
all_driver_metadata = AllDriverMetadata(version=VERSION)


@summary_api_blueprint.route('/api/alldrivers/summary/', methods=['GET'])
def get_summary():
    summary_data = all_driver_summary.get_summary()
    return jsonify({
        'success': True,
        **summary_data
    })


@summary_api_blueprint.route('/api/alldrivers/metadata/', methods=['GET'])
def get_summary_meta_data():
    metadata = all_driver_metadata.get_metadata()
    return jsonify({
        'success': True,
        **metadata
    })
