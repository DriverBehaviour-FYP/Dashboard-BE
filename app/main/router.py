from app.main.routes.home_route import home_api_blueprint
from app.main.routes.driver_route import driver_api_blueprint
from app.main.routes.cluster_prediction_route import clusterp_api_blueprint
from app.main.routes.forecast_info_route import forecast_api_blueprint
from app.main.routes.summary_route import summary_api_blueprint
from app.main.routes.trip_route import trip_api_blueprint


def register_routes(app):
    app.register_blueprint(driver_api_blueprint)
    app.register_blueprint(clusterp_api_blueprint)
    app.register_blueprint(forecast_api_blueprint)
    app.register_blueprint(home_api_blueprint)
    app.register_blueprint(summary_api_blueprint)
    app.register_blueprint(trip_api_blueprint)
    return app
