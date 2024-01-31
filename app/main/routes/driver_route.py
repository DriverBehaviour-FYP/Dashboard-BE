from flask import Blueprint, jsonify
from app.main.controllers.driver.driver_metadata_cache import DriverMetadata
from app.main.controllers.driver.driver_summary_cache import DriverSummary

driver_api_blueprint = Blueprint("api/driver", __name__)

global driver_metadata;
global driver_summary;

driver_metadata = DriverMetadata(version='10T')
driver_summary = DriverSummary(version='10T')


@driver_api_blueprint.route('/api/driver/<driver_id>', methods=['GET'])
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
