from flask import Blueprint, jsonify

home_api_blueprint = Blueprint("api/home", __name__)


@home_api_blueprint.route('/api/home/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is driver API.'})
