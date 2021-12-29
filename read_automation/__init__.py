from flask import Flask


######################################
#### Application Factory Function ####
######################################

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    register_blueprints(app)
    register_error_pages(app)
    return app


########################
### Helper Functions ###
########################

def register_blueprints(app):
    # Import the blueprints
    from read_automation.temperature import temperature_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(temperature_blueprint)


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return "404 not found"
