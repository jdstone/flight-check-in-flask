from app.extensions import scheduler # WORKS-kinda
import atexit
from config import config
from flask import Flask
import logging
import os
import requests

from datetime import datetime
import time



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
    
    from . import checkin
    app.register_blueprint(checkin.bp)

    ###################################################
    #### Initialize Extensions
    ###################################################
    scheduler.init_app(app)
    # with app.app_context():
    #     try:
    #         scheduler.start()
    #     except (KeyboardInterrupt, SystemExit):
    #         pass
    try:
        scheduler.start() # APScheduler WORKS-kinda
    except (KeyboardInterrupt, SystemExit):
        pass
    # scheduler.start()

    # logger = logging.get_logger('apscheduler')
    # logger.setLevel(logging.DEBUG)
    # logging.getLogger("apscheduler").setLevel(logging.DEBUG)

    # @app.teardown_appcontext ## causes problem when accessing the API, so this is probably wrong
    # def stop_scheduler(exception=None):
    #     scheduler.shutdown()

    return app

