from flask import Blueprint, jsonify

summary_api_blueprint = Blueprint("api/summary", __name__)


@summary_api_blueprint.route('/api/summary/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is summary API.'})
