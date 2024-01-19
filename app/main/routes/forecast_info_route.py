from flask import Blueprint, jsonify

forecast_api_blueprint = Blueprint("api/forecast", __name__)


@forecast_api_blueprint.route('/api/forecast/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is forecast API.'})
