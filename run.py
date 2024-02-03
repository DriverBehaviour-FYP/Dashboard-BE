from flask import Flask, jsonify
from app.main.router import register_routes
from flask_cors import CORS

# create flask app
app = Flask(__name__)
# Register the API blueprints
app = register_routes(app)

CORS(app)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# run main application
if __name__ == '__main__':
    app.run(debug=True)
