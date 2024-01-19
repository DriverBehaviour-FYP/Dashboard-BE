from flask import Blueprint, jsonify

trip_api_blueprint = Blueprint("api/trip", __name__)


@trip_api_blueprint.route('/api/trip/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is trip API.'})
