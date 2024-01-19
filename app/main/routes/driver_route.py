from flask import Blueprint, jsonify

driver_api_blueprint = Blueprint("api/driver", __name__)


@driver_api_blueprint.route('/api/driver/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is driver API.'})
