from flask import Flask
from app.main.router import register_routes

# create flask app
app = Flask(__name__)

# Register the API blueprints
app = register_routes(app)

# run main application
if __name__ == '__main__':
    app.run(debug=True)
