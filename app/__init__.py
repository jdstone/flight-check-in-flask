from config import config
from flask import Flask
from flask_apscheduler import APScheduler
import os
import requests


def create_app(config_class=os.getenv('FLASK_ENV') or 'default'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_class])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ###################################################
    #### Register Blueprints
    ###################################################
    from . import southwest
    app.register_blueprint(southwest.bp)

    return app

