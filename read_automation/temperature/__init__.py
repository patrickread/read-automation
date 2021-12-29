from flask import Blueprint

temperature_blueprint = Blueprint("temp", __name__)

from . import routes
